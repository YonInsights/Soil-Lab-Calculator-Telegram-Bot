# calculations.py

def calculate_moisture_content(wet_weight, dry_weight):
    return (wet_weight - dry_weight) / dry_weight * 100

def calculate_liquid_limit(cone_penetration_values, water_contents):
    # Liquid Limit is interpolated based on penetration and water content values
    # Assuming cone_penetration_values and water_contents are paired lists
    penetration_at_20mm = 20  # Example penetration target
    # Placeholder for interpolation logic
    return sum(water_contents) / len(water_contents)  # Simplified average as placeholder

def calculate_plastic_limit(plastic_limit_value):
    return plastic_limit_value

def calculate_plasticity_index(liquid_limit, plastic_limit):
    return liquid_limit - plastic_limit

def calculate_shrinkage_limit(initial_volume, final_volume, volume_of_water_lost):
    return (initial_volume - final_volume) / volume_of_water_lost * 100

def calculate_field_density_sand_replacement(weight_of_sand_filled, bulk_density_of_sand):
    return weight_of_sand_filled / bulk_density_of_sand

def calculate_field_density_core_cutter(mass_of_soil_core, core_volume, moisture_content):
    bulk_density = mass_of_soil_core / core_volume
    return bulk_density / (1 + moisture_content / 100)

def calculate_linear_shrinkage(initial_length, final_length):
    return (initial_length - final_length) / initial_length * 100

def calculate_particle_size_distribution(weight_retained, total_weight):
    return (1 - (weight_retained / total_weight)) * 100

def calculate_hydrometer(penetration_depth, fluid_viscosity, specific_gravity):
    """
    Calculate particle diameter using hydrometer analysis based on Stokes' Law.
    
    Args:
        penetration_depth (float): Depth of penetration (meters).
        fluid_viscosity (float): Viscosity of fluid (Pa·s).
        specific_gravity (float): Specific gravity of soil particles.

    Returns:
        float: Particle diameter (mm).
    """
    g = 9.81  # Gravitational acceleration (m/s^2)
    water_specific_gravity = 1  # Default specific gravity of water
    numerator = 18 * fluid_viscosity * penetration_depth
    denominator = (specific_gravity - water_specific_gravity) * g

    if denominator <= 0:
        raise ValueError("Invalid specific gravity. Ensure soil specific gravity is greater than 1.")
    
    particle_diameter = (numerator / denominator) ** 0.5
    return particle_diameter * 1000  # Convert to mm
def calculate_compaction_test(bulk_density, moisture_content):
    return bulk_density / (1 + moisture_content / 100)

def calculate_cbr(force_applied, standard_force):
    return (force_applied / standard_force) * 100

def calculate_specific_gravity(mass_of_dry_soil, mass_of_displaced_water):
    return mass_of_dry_soil / mass_of_displaced_water

def calculate_material_finer_no_200(initial_mass, final_mass):
    return ((initial_mass - final_mass) / initial_mass) * 100

def calculate_moisture_density_relationship(dry_density, moisture_content):
    return dry_density * (1 + moisture_content / 100)

def calculate_volume_metric(initial_volume, final_volume):
    return initial_volume - final_volume  # Adjust logic based on actual requirements

def calculate_mechanical_analysis(weight_passed, total_weight):
    return (weight_passed / total_weight) * 100

def calculate_cbr_force_based(force_applied, penetration_depth):
    standard_force_2_5mm = 13.24  # kN
    standard_force_5mm = 19.96  # kN
    if penetration_depth == 2.5:
        return (force_applied / standard_force_2_5mm) * 100
    elif penetration_depth == 5:
        return (force_applied / standard_force_5mm) * 100
    else:
        return "Invalid penetration depth"

def calculate_unified_classification(plasticity_index, liquid_limit):
    # Add classification logic based on Unified Soil Classification System
    return "Unified Classification Result"  # Placeholder

def calculate_aashto_classification(soil_properties):
    # Add classification logic based on AASHTO soil classification
    return "AASHTO Classification Result"  # Placeholder

def calculate_hydrometer_properties(hydrometer_reading, temperature, specific_gravity):
    # Add logic for hydrometer analysis based on the reading and temperature
    return "Hydrometer Analysis Result"  # Placeholder

def calculate_in_place_density(mass_of_soil, volume_of_soil):
    return mass_of_soil / volume_of_soil
