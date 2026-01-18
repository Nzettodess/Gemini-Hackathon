
from codecarbon import EmissionsTracker
import functools
import traceback
from typing import Dict, Any, Callable

def track_energy_impact(func: Callable) -> Callable:
    """
    Decorator to track the energy impact of a function call.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        tracker = EmissionsTracker(
            project_name="data_governance_task",
            measure_power_secs=1,
            output_dir=".",
            save_to_file=False,
            log_level="error"
        )
        tracker.start()
        try:
            result = func(*args, **kwargs)
        finally:
            emissions = tracker.stop()
        
        # If the result is a dict (our standard tool output), append energy stats
        if isinstance(result, dict):
            result["_energy_impact"] = {
                "emissions_kg": emissions,
                "energy_consumed_kwh": tracker.final_emissions_data.energy_consumed,
                "duration_seconds": tracker.final_emissions_data.duration
            }
        return result
    return wrapper

def estimate_carbon_footprint(duration_seconds: float, hardware_type: str = "cpu") -> Dict[str, Any]:
    """
    Estimates carbon footprint based on duration and hardware type (mock/heuristic for when direct measurement isn't possible).
    """
    # Average power consumption in Watts
    power_map = {
        "cpu": 150,  # Standard Server CPU
        "gpu_t4": 70,
        "gpu_a100": 400
    }
    power_watts = power_map.get(hardware_type.lower(), 100)
    
    # Global average carbon intensity (gCO2/kWh) - approx 475
    carbon_intensity = 475 
    
    energy_kwh = (power_watts * duration_seconds) / (1000 * 3600)
    emissions_kg = (energy_kwh * carbon_intensity) / 1000
    
    return {
        "estimated_emissions_kg": emissions_kg,
        "estimated_energy_kwh": energy_kwh,
        "assumptions": f"Power: {power_watts}W, Carbon Intensity: {carbon_intensity} gCO2/kWh"
    }
