import os
import uuid
from datetime import datetime
from openlineage.client import OpenLineageClient
from openlineage.client.transport.console import ConsoleTransport, ConsoleConfig
from openlineage.client.run import RunEvent, RunState, Run, Job
from openlineage.client.facet import NominalTimeRunFacet

# Initialize client with Console transport by default
# In production, this would be an HTTP transport
client = OpenLineageClient(transport=ConsoleTransport(config=ConsoleConfig()))

def emit_lineage_start(job_name: str, namespace: str = "data_governance_system") -> str:
    """
    Emits a START run event.
    Returns the run_id.
    """
    run_id = str(uuid.uuid4())
    event_time = datetime.now().isoformat()
    
    run_event = RunEvent(
        eventType=RunState.START,
        eventTime=event_time,
        run=Run(runId=run_id, facets={
            "nominalTime": NominalTimeRunFacet(
                nominalStartTime=event_time,
                nominalEndTime=event_time # Just a placeholder
            )
        }),
        job=Job(namespace=namespace, name=job_name),
        inputs=[],
        outputs=[],
        producer="data_governance_mcp_agent"
    )
    
    client.emit(run_event)
    return run_id

def emit_lineage_complete(run_id: str, job_name: str, namespace: str = "data_governance_system"):
    """
    Emits a COMPLETE run event.
    """
    event_time = datetime.now().isoformat()
    
    run_event = RunEvent(
        eventType=RunState.COMPLETE,
        eventTime=event_time,
        run=Run(runId=run_id),
        job=Job(namespace=namespace, name=job_name),
        inputs=[],
        outputs=[],
        producer="data_governance_mcp_agent"
    )
    
    client.emit(run_event)
