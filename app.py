from flask import Flask, render_template, request
import math

app = Flask(__name__)

# Main page with different cards
@app.route('/')
def index():
    return render_template('index.html')

# Logic for Page 1
@app.route('/page1', methods=['GET', 'POST'])
def page1():
    if request.method == 'POST':
        # Get the form inputs
        num_mouldboards = int(request.form['num_mouldboards'])
        num_bottoms = int(request.form['num_bottoms'])
        width_of_cut = float(request.form['width_of_cut'])
        actual_time_taken = float(request.form['actual_time_taken'])
        actual_distance_traveled = float(request.form['actual_distance_traveled'])
        average_speed = float(request.form['average_speed'])

        # Call the calculate_field_efficiency function
        result = mb_calculate_field_efficiency(num_mouldboards, num_bottoms, width_of_cut, actual_time_taken,
                                            actual_distance_traveled, average_speed)

        # Return the result to the page
        return render_template('page1.html', result=f"{result:.2f}")
    
    return render_template('page1.html', result=None)

def mb_calculate_field_efficiency(num_mouldboards, num_bottoms, width_of_cut, actual_time_taken, actual_distance_traveled,
                                average_speed):
    # Calculate theoretical field capacity (hectares/hour)
    theoretical_field_capacity = (num_mouldboards * num_bottoms * width_of_cut * average_speed) / 10  # hectares/hour

    # Calculate actual field capacity (hectares/hour)
    actual_field_capacity = (actual_distance_traveled / 1000) / (actual_time_taken / 3600)  # hectares/hour

    # Calculate field efficiency (%)
    field_efficiency = (actual_field_capacity / theoretical_field_capacity) * 100  
    
    return field_efficiency





# Logic for Page 2
# Field efficiency calculation function
def calculate_field_efficiency(speed, width_of_cut, field_area, total_time):
    """
    Calculate the field efficiency of a disk plow.

    Parameters:
    speed (float): Tractor speed in km/h
    width_of_cut (float): Width of cut in meters
    field_area (float): Total field area in hectares
    total_time (float): Total time taken in hours

    Returns:
    float: Field efficiency in percentage
    """
    # Calculate Effective Field Capacity (EFC)
    efc = field_area / total_time

    # Calculate Theoretical Field Capacity (TFC)
    tfc = speed * width_of_cut * 0.1  # 0.1 is the conversion factor

    # Calculate Field Efficiency
    field_efficiency = (efc / tfc) * 100

    return field_efficiency


@app.route('/page2')
def page2():
    return render_template('page2.html')


@app.route('/calculate_efficiency', methods=['POST'])
def calculate_efficiency():
    try:
        # Get user inputs
        speed = float(request.form['speed'])
        width_of_cut = float(request.form['width_of_cut'])
        field_area = float(request.form['field_area'])
        total_time = float(request.form['total_time'])

        # Calculate field efficiency
        efficiency = calculate_field_efficiency(speed, width_of_cut, field_area, total_time)
        
        # Render the result on the same page with the result
        return render_template('page2.html', field_efficiency=f"{efficiency:.2f}")

    except ValueError:
        return render_template('page2.html', error="Invalid input. Please enter numeric values.")









# Logic for Page 3

# Function to calculate theoretical field capacity
def harrow_calculate_tfc(width, speed):
    return width * speed * 0.1  # Theoretical Field Capacity (ha/h)

# Function to calculate actual field capacity
def harrow_calculate_afc(area, time):
    return area / time  # Actual Field Capacity (ha/h)

# Function to calculate field efficiency
def harrow_calculate_field_efficiency(afc, tfc):
    return (afc / tfc) * 100  # Field efficiency as percentage

# Function to calculate disc spacing using provided formula
def harrow_calculate_spacing(ridge_height, disc_diameter, gang_angle):
    return 2 * math.sqrt(ridge_height * (disc_diameter - ridge_height)) * math.tan(math.radians(gang_angle))

# Function to calculate cutting width for single-acting disc harrow (IS standard)
def harrow_calculate_cutting_width_single_acting(N, spacing, disc_diameter):
    return (0.95 * N * spacing + 0.6 * disc_diameter) / 100  # Width in meters

# Function to calculate cutting width for offset disc harrow (ASAE standard)
def harrow_calculate_cutting_width_offset(N1, spacing, disc_diameter):
    return (0.95 * (N1 - 2) * spacing + 0.6 * disc_diameter) / 100  # Width in meters

@app.route('/harrow', methods=['GET', 'POST'])
def harrow_calculator():
    if request.method == 'POST':
        try:
            # Get form data
            speed = float(request.form['speed'])
            area = float(request.form['area'])
            time = float(request.form['time'])
            ridge_height = float(request.form['ridge_height'])
            gang_angle = float(request.form['gang_angle'])
            disc_diameter = float(request.form['disc_diameter'])
            harrow_type = int(request.form['harrow_type'])  # 1 for single-acting, 2 for offset

            if harrow_type == 1:  # Single-Acting Disc Harrow
                N = int(request.form['N'])  # Number of disc spacings
                spacing = harrow_calculate_spacing(ridge_height, disc_diameter, gang_angle)
                cutting_width = harrow_calculate_cutting_width_single_acting(N, spacing, disc_diameter)
            elif harrow_type == 2:  # Offset Disc Harrow
                N1 = int(request.form['N1'])  # Number of disc blades
                spacing = harrow_calculate_spacing(ridge_height, disc_diameter, gang_angle)
                cutting_width = harrow_calculate_cutting_width_offset(N1, spacing, disc_diameter)
            else:
                return "Invalid harrow type selected."

            # Calculate Theoretical Field Capacity (TFC) and Actual Field Capacity (AFC)
            tfc = harrow_calculate_tfc(cutting_width, speed)
            afc = harrow_calculate_afc(area, time)

            # Calculate field efficiency
            field_efficiency = harrow_calculate_field_efficiency(afc, tfc)

            # Pass results to the template
            return render_template('page3.html', tfc=tfc, afc=afc, field_efficiency=field_efficiency, 
                                   spacing=spacing, cutting_width=cutting_width)
        except ValueError:
            return "Invalid input. Please ensure all values are numeric."
    return render_template('page3.html')









# Logic for Page 4
def cult_calculate_tfc(implement_width, speed):
    tfc = (implement_width * speed) / 10
    return tfc

# Function to calculate Effective Field Capacity (EFC)
def cult_calculate_efc(area_covered, time_spent):
    efc = area_covered / time_spent
    return efc

# Function to calculate Field Efficiency
def cult_calculate_field_efficiency(efc, tfc):
    efficiency = (efc / tfc) * 100
    return efficiency

@app.route('/cultivator', methods=['GET', 'POST'])
def cultivator():
    results = None
    if request.method == 'POST':
        # Get input data from the form
        num_of_tines = int(request.form['num_of_tines'])
        tine_spacing = float(request.form['tine_spacing'])
        speed = float(request.form['speed'])
        area_covered = float(request.form['area_covered'])
        time_spent = float(request.form['time_spent'])
        time_loss_percent = float(request.form['time_loss_percent'])

        # Calculate actual time spent
        actual_time_spent = time_spent * ((100 - time_loss_percent) / 100)

        # Calculate implement width
        implement_width = num_of_tines * tine_spacing

        # Calculate TFC and EFC
        tfc = cult_calculate_tfc(implement_width, speed)
        efc = cult_calculate_efc(area_covered, actual_time_spent)

        # Calculate field efficiency
        efficiency = cult_calculate_field_efficiency(efc, tfc)

        # Prepare results for rendering
        results = {
            'tfc': f"{tfc:.2f}",
            'efc': f"{efc:.2f}",
            'efficiency': f"{efficiency:.2f}",
        }

    return render_template('page4.html', results=results)









# Logic for Page 5
@app.route('/page5', methods=['GET', 'POST'])
def page5():
    if request.method == 'POST':
        data = request.form.get('data')
        result = f"Processed data: {data}"
        return render_template('page5.html', result=result)
    return render_template('page5.html', result=None)

# Logic for Page 6
@app.route('/page6', methods=['GET', 'POST'])
def page6():
    if request.method == 'POST':
        data = request.form.get('data')
        result = f"Processed data: {data}"
        return render_template('page6.html', result=result)
    return render_template('page6.html', result=None)

# Logic for Page 7
@app.route('/page7', methods=['GET', 'POST'])
def page7():
    if request.method == 'POST':
        data = request.form.get('data')
        result = f"Processed data: {data}"
        return render_template('page7.html', result=result)
    return render_template('page7.html', result=None)

# Logic for Page 8
@app.route('/page8', methods=['GET', 'POST'])
def page8():
    if request.method == 'POST':
        data = request.form.get('data')
        result = f"Processed data: {data}"
        return render_template('page8.html', result=result)
    return render_template('page8.html', result=None)

if __name__ == '__main__':
    app.run(debug=True)
