"""
Performance metrics API endpoints (ST-013).

Provides access to latency and error rate metrics for monitoring
and SLA compliance.
"""
from typing import List, Dict

from fastapi import APIRouter, Depends, Query

from app.middleware.performance import get_latency_metrics, get_endpoint_metrics, LATENCY_BUDGETS, ERROR_RATE_BUDGET
from app.api.deps import require_role
from app.models.user import User

router = APIRouter(prefix="/performance", tags=["performance"])


@router.get("/metrics", response_model=List[Dict])
async def get_all_performance_metrics(
    current_user: User = Depends(require_role("admin"))
):
    """
    Get performance metrics for all endpoints.
    
    Returns latency percentiles (P50, P95, P99) and error rates.
    Requires admin role.
    
    Returns:
        - **endpoint**: Endpoint path
        - **request_count**: Total requests
        - **error_count**: Total errors
        - **error_rate**: Error rate (0.0-1.0)
        - **latency_p50_ms**: P50 latency in milliseconds
        - **latency_p95_ms**: P95 latency in milliseconds
        - **latency_p99_ms**: P99 latency in milliseconds
    """
    metrics = get_latency_metrics()
    
    # Add budget information
    for metric in metrics:
        endpoint = metric["endpoint"]
        if endpoint in LATENCY_BUDGETS:
            metric["latency_budget"] = LATENCY_BUDGETS[endpoint]
            metric["p95_within_budget"] = metric["latency_p95_ms"] <= LATENCY_BUDGETS[endpoint]["p95"]
            metric["p99_within_budget"] = metric["latency_p99_ms"] <= LATENCY_BUDGETS[endpoint]["p99"]
        
        metric["error_budget"] = ERROR_RATE_BUDGET
        metric["error_rate_within_budget"] = metric["error_rate"] <= ERROR_RATE_BUDGET
    
    return metrics


@router.get("/metrics/{endpoint:path}")
async def get_endpoint_performance_metrics(
    endpoint: str,
    current_user: User = Depends(require_role("admin"))
):
    """
    Get performance metrics for a specific endpoint.
    
    Requires admin role.
    
    Args:
        endpoint: The endpoint path (e.g., /api/v1/jobs)
    """
    metric = get_endpoint_metrics(endpoint)
    
    # Add budget information
    if endpoint in LATENCY_BUDGETS:
        metric["latency_budget"] = LATENCY_BUDGETS[endpoint]
        metric["p95_within_budget"] = metric["latency_p95_ms"] <= LATENCY_BUDGETS[endpoint]["p95"]
        metric["p99_within_budget"] = metric["latency_p99_ms"] <= LATENCY_BUDGETS[endpoint]["p99"]
    
    metric["error_budget"] = ERROR_RATE_BUDGET
    metric["error_rate_within_budget"] = metric["error_rate"] <= ERROR_RATE_BUDGET
    
    return metric


@router.get("/budgets")
async def get_sla_budgets(
    current_user: User = Depends(require_role("admin"))
):
    """
    Get defined SLA budgets for all endpoints.
    
    Returns latency budgets (P95, P99) and error rate budget.
    Requires admin role.
    """
    return {
        "latency_budgets": LATENCY_BUDGETS,
        "error_rate_budget": ERROR_RATE_BUDGET,
        "budget_description": {
            "latency_budgets": "P95 and P99 latency targets in milliseconds",
            "error_rate_budget": "Maximum acceptable error rate (decimal, e.g., 0.01 = 1%)"
        }
    }


@router.get("/violations")
async def get_budget_violations(
    current_user: User = Depends(require_role("admin"))
):
    """
    Get endpoints that are currently violating SLA budgets.
    
    Returns list of endpoints exceeding latency or error rate budgets.
    Requires admin role.
    """
    metrics = get_latency_metrics()
    violations = []
    
    for metric in metrics:
        endpoint = metric["endpoint"]
        endpoint_violations = []
        
        # Check latency budgets
        if endpoint in LATENCY_BUDGETS:
            budget = LATENCY_BUDGETS[endpoint]
            
            if metric["latency_p95_ms"] > budget["p95"]:
                endpoint_violations.append({
                    "type": "latency_p95",
                    "current": metric["latency_p95_ms"],
                    "budget": budget["p95"],
                    "excess_ms": metric["latency_p95_ms"] - budget["p95"]
                })
            
            if metric["latency_p99_ms"] > budget["p99"]:
                endpoint_violations.append({
                    "type": "latency_p99",
                    "current": metric["latency_p99_ms"],
                    "budget": budget["p99"],
                    "excess_ms": metric["latency_p99_ms"] - budget["p99"]
                })
        
        # Check error rate budget
        if metric["error_rate"] > ERROR_RATE_BUDGET:
            endpoint_violations.append({
                "type": "error_rate",
                "current": metric["error_rate"],
                "budget": ERROR_RATE_BUDGET,
                "excess": metric["error_rate"] - ERROR_RATE_BUDGET
            })
        
        if endpoint_violations:
            violations.append({
                "endpoint": endpoint,
                "violations": endpoint_violations,
                "metrics": metric
            })
    
    return {
        "violation_count": len(violations),
        "violations": violations
    }
