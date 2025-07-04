from typing import Dict, Any, List, Optional, Callable
import asyncio
import json
import time
from datetime import datetime
from ..core.database import get_db
from sqlalchemy.orm import Session

class EvaluationMetric:
    """Base class for evaluation metrics"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    async def evaluate(self, input_data: Dict[str, Any], output_data: Dict[str, Any], expected_output: Dict[str, Any] = None) -> Dict[str, Any]:
        """Evaluate agent performance"""
        raise NotImplementedError

class AccuracyMetric(EvaluationMetric):
    """Accuracy evaluation metric"""
    
    def __init__(self):
        super().__init__("accuracy", "Measures correctness of agent responses")
    
    async def evaluate(self, input_data: Dict[str, Any], output_data: Dict[str, Any], expected_output: Dict[str, Any] = None) -> Dict[str, Any]:
        if not expected_output:
            return {"score": None, "error": "No expected output provided"}
        
        # Simple string comparison for now - can be enhanced with semantic similarity
        actual = str(output_data.get("result", "")).lower().strip()
        expected = str(expected_output.get("result", "")).lower().strip()
        
        score = 1.0 if actual == expected else 0.0
        
        return {
            "score": score,
            "details": {
                "actual": actual,
                "expected": expected,
                "match": score == 1.0
            }
        }

class LatencyMetric(EvaluationMetric):
    """Response time evaluation metric"""
    
    def __init__(self, threshold_seconds: float = 5.0):
        super().__init__("latency", "Measures agent response time")
        self.threshold = threshold_seconds
    
    async def evaluate(self, input_data: Dict[str, Any], output_data: Dict[str, Any], expected_output: Dict[str, Any] = None) -> Dict[str, Any]:
        execution_time = output_data.get("execution_time", 0)
        
        # Score based on threshold (1.0 if under threshold, scaled down if over)
        if execution_time <= self.threshold:
            score = 1.0
        else:
            score = max(0.0, 1.0 - (execution_time - self.threshold) / self.threshold)
        
        return {
            "score": score,
            "details": {
                "execution_time": execution_time,
                "threshold": self.threshold,
                "under_threshold": execution_time <= self.threshold
            }
        }

class SuccessRateMetric(EvaluationMetric):
    """Success rate evaluation metric"""
    
    def __init__(self):
        super().__init__("success_rate", "Measures successful completion rate")
    
    async def evaluate(self, input_data: Dict[str, Any], output_data: Dict[str, Any], expected_output: Dict[str, Any] = None) -> Dict[str, Any]:
        status = output_data.get("status", "failed")
        score = 1.0 if status == "completed" else 0.0
        
        return {
            "score": score,
            "details": {
                "status": status,
                "successful": score == 1.0,
                "error": output_data.get("error")
            }
        }

class EvaluationFramework:
    """Framework for evaluating agent performance"""
    
    def __init__(self):
        self.metrics = {}
        self.test_suites = {}
        self._register_default_metrics()
    
    def _register_default_metrics(self):
        """Register default evaluation metrics"""
        self.register_metric(AccuracyMetric())
        self.register_metric(LatencyMetric())
        self.register_metric(SuccessRateMetric())
    
    def register_metric(self, metric: EvaluationMetric):
        """Register a new evaluation metric"""
        self.metrics[metric.name] = metric
    
    def create_test_suite(self, name: str, test_cases: List[Dict[str, Any]]):
        """Create a test suite with multiple test cases"""
        self.test_suites[name] = {
            "name": name,
            "test_cases": test_cases,
            "created_at": datetime.utcnow().isoformat()
        }
    
    async def evaluate_agent(self, agent, test_suite_name: str, metrics: List[str] = None) -> Dict[str, Any]:
        """Evaluate an agent against a test suite"""
        if test_suite_name not in self.test_suites:
            raise ValueError(f"Test suite '{test_suite_name}' not found")
        
        test_suite = self.test_suites[test_suite_name]
        metrics_to_use = metrics or list(self.metrics.keys())
        
        results = {
            "agent_name": agent.name,
            "test_suite": test_suite_name,
            "started_at": datetime.utcnow().isoformat(),
            "test_results": [],
            "summary": {}
        }
        
        for i, test_case in enumerate(test_suite["test_cases"]):
            test_result = await self._run_test_case(agent, test_case, metrics_to_use, i)
            results["test_results"].append(test_result)
        
        # Calculate summary statistics
        results["summary"] = self._calculate_summary(results["test_results"], metrics_to_use)
        results["completed_at"] = datetime.utcnow().isoformat()
        
        return results
    
    async def _run_test_case(self, agent, test_case: Dict[str, Any], metrics: List[str], test_index: int) -> Dict[str, Any]:
        """Run a single test case"""
        input_data = test_case["input"]
        expected_output = test_case.get("expected_output")
        
        # Execute agent
        start_time = time.time()
        try:
            output_data = await agent.execute(input_data)
            execution_time = time.time() - start_time
            output_data["execution_time"] = execution_time
        except Exception as e:
            execution_time = time.time() - start_time
            output_data = {
                "status": "failed",
                "error": str(e),
                "execution_time": execution_time
            }
        
        # Evaluate with each metric
        metric_results = {}
        for metric_name in metrics:
            if metric_name in self.metrics:
                metric = self.metrics[metric_name]
                try:
                    metric_result = await metric.evaluate(input_data, output_data, expected_output)
                    metric_results[metric_name] = metric_result
                except Exception as e:
                    metric_results[metric_name] = {"score": None, "error": str(e)}
        
        return {
            "test_index": test_index,
            "input": input_data,
            "output": output_data,
            "expected_output": expected_output,
            "metrics": metric_results,
            "execution_time": execution_time
        }
    
    def _calculate_summary(self, test_results: List[Dict[str, Any]], metrics: List[str]) -> Dict[str, Any]:
        """Calculate summary statistics"""
        summary = {
            "total_tests": len(test_results),
            "metrics_summary": {}
        }
        
        for metric_name in metrics:
            scores = []
            for result in test_results:
                metric_result = result["metrics"].get(metric_name, {})
                score = metric_result.get("score")
                if score is not None:
                    scores.append(score)
            
            if scores:
                summary["metrics_summary"][metric_name] = {
                    "average_score": sum(scores) / len(scores),
                    "min_score": min(scores),
                    "max_score": max(scores),
                    "total_evaluated": len(scores)
                }
            else:
                summary["metrics_summary"][metric_name] = {
                    "average_score": None,
                    "error": "No valid scores"
                }
        
        return summary
    
    async def continuous_evaluation(self, agent, test_suite_name: str, interval_minutes: int = 60):
        """Run continuous evaluation at specified intervals"""
        while True:
            try:
                results = await self.evaluate_agent(agent, test_suite_name)
                
                # Store results (could be enhanced to save to database)
                print(f"Evaluation completed for {agent.name}: {results['summary']}")
                
                # Wait for next evaluation
                await asyncio.sleep(interval_minutes * 60)
                
            except Exception as e:
                print(f"Continuous evaluation error: {e}")
                await asyncio.sleep(60)  # Wait 1 minute before retry

# Global evaluation framework
evaluation_framework = EvaluationFramework()

# Example test suite for TAMS agent
TAMS_TEST_SUITE = [
    {
        "input": {"alert_id": 1, "query": "Check alert status"},
        "expected_output": {"status": "completed", "result": {"alert_status": "processed"}}
    },
    {
        "input": {"alert_id": 2, "query": "Analyze security alert"},
        "expected_output": {"status": "completed", "result": {"risk_level": "medium"}}
    },
    {
        "input": {"alert_id": 999, "query": "Non-existent alert"},
        "expected_output": {"status": "failed", "error": "Alert not found"}
    }
]

# Initialize TAMS test suite
evaluation_framework.create_test_suite("tams_basic", TAMS_TEST_SUITE)