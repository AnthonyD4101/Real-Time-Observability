import httpx, asyncio, time
from faker import Faker
from models import ExplorationProduction, FinancialPerformance, HealthSafetyEnvironment

mock_data = Faker()

def generate_fake_exploration_production():
    return ExplorationProduction(
        timestamp = mock_data.date_time().isoformat(),
        event_id = mock_data.uuid4(),
        drilling_success_rate = mock_data.pyfloat(left_digits = 1, right_digits = 2, positive = True),
        throughput_production_rate = mock_data.pyfloat(left_digits = 3, right_digits = 2, positive = True),
        quality = mock_data.random_element(elements = ('high', 'medium', 'low')),
        machine_downtime = mock_data.pyfloat(left_digits = 1, right_digits = 2, positive = True),
        operational_efficiency = mock_data.pyfloat(left_digits = 1, right_digits = 2, positive = True),
        roi = mock_data.pyfloat(left_digits = 1, right_digits = 2, positive = True),
    )

def generate_fake_financial_performance():
    return FinancialPerformance(
        timestamp = mock_data.date_time().isoformat(),
        event_id = mock_data.uuid4(),
        revenue = mock_data.pyfloat(left_digits = 5, right_digits = 2, positive = True),
        net_income = mock_data.pyfloat(left_digits = 5, right_digits = 2, positive = True),
        cash_flow = mock_data.pyfloat(left_digits = 5, right_digits = 2, positive = True),
    )

def generate_fake_health_safety_environment():
    return HealthSafetyEnvironment(
        timestamp = mock_data.date_time().isoformat(),
        event_id = mock_data.uuid4(),
        lost_time_incident_rate = mock_data.pyfloat(left_digits = 1, right_digits = 2, positive = True),
        environmental_compliance_rate = mock_data.pyfloat(left_digits = 1, right_digits = 2, positive = True),
        greenhouse_gas_emissions = mock_data.pyfloat(left_digits = 3, right_digits = 2, positive = True),
    )

async def send_fake_data():
    async with httpx.AsyncClient(timeout=10.0) as client:
        while True:
            exploration_data = generate_fake_exploration_production()
            financial_data = generate_fake_financial_performance()
            hse_data = generate_fake_health_safety_environment()

            await client.post("http://localhost:8080/add_exploration_production", json = exploration_data.model_dump())
            await client.post("http://localhost:8080/add_financial_performance", json = financial_data.model_dump())
            await client.post("http://localhost:8080/add_health_safety_environment", json = hse_data.model_dump())

            print("Fake data sent to all endpoints.")
            await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(send_fake_data())