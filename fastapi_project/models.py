from pydantic import BaseModel

class ExplorationProduction(BaseModel):
    timestamp: str
    event_id: str
    drilling_success_rate: float
    throughput_production_rate: float
    quality: str
    machine_downtime: float
    operational_efficiency: float
    roi: float

class FinancialPerformance(BaseModel):
    timestamp: str
    event_id: str
    revenue: float
    net_income: float
    cash_flow: float

class HealthSafetyEnvironment(BaseModel):
    timestamp: str
    event_id: str
    lost_time_incident_rate: float
    environmental_compliance_rate: float
    greenhouse_gas_emissions: float
