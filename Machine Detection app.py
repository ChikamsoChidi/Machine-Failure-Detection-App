import customtkinter as ctk
import pandas as pd
import pickle
import os


## CTK Configuration
# Set the overall appearance mode for the application
ctk.set_appearance_mode('light')

# Set the default color theme
ctk.set_default_color_theme('blue')

class MachineDetectApp(ctk.CTk):
    """
    A CustomTkinter application for predicting machine failure 
    based on various sensor and operational readings.
    """
    def __init__(self, model_path: str = "model.pkl", *args, **kwargs):
        """
        Initializes the application, sets up the window, and creates all widgets.

        Args:
            model_path (str): The file path to the pickled machine learning model.
        """
        # Initialize the parent class (ctk.CTk), setting up the main window structure.
        super().__init__(*args, **kwargs)
        
        # Store the model path
        self.model_path = model_path
        
        ## Window Setup
        self.title('Machine Failure Detection App')
        # Set a fixed size for the window
        self.geometry('420x530') 
        
        # Configure grid weights to ensure columns adjust correctly if content size changes
        self.grid_columnconfigure(0, weight=0) # Column 0 for labels
        self.grid_columnconfigure(1, weight=1) # Column 1 for entry fields

        ## Widget Creation and Layout
        # The variables below store the CTkEntry objects for later data retrieval
    
        # 1. Footfall
        self._create_input_row('Foot fall', 1, 'footfall')
        
        # 2. Temperature Mode (The set-point or desired temperature)
        self._create_input_row('Temperature Mode', 2, 'tempMode')
        
        # 3. Air Quality
        self._create_input_row('Air Quality', 3, 'airQuality')
        
        # 4. UltraSonic Sensor reading (USS)
        self._create_input_row('UltraSonic Sensor reading', 4, 'ultraSonicSensor')
        
        # 5. Electrical Current (CS)
        self._create_input_row('Electric Current', 5, 'electricalCurrentReading')
        
        # 6. Volatile Organic Compound Levels (VOC)
        self._create_input_row('Volatile Organic Compound Levels', 6, 'VOC')
        
        # 7. Rotations Per Minute (RPM)
        self._create_input_row('Rotations Per Minute', 7, 'RPM')
        
        # 8. Input Pressure (IP)
        self._create_input_row('Input Pressure', 8, 'InputPressure')

        # 9. Current Measured Temperature
        self._create_input_row('Temperature', 9, 'Temperature')
        
        # 10. Average RPM Difference (RP_Avg)
        self._create_input_row('Average RPM Difference', 10, 'AverageRPM_Diff')
        
        
        ## Submission Button
        self.SubmitButton = ctk.CTkButton(
            self, 
            text='Submit', 
            command=self.submit_prediction
        )
        # Place button in the second column (below entries)
        self.SubmitButton.grid(row=11, column=1, padx=20, pady=10, sticky='E')
        
        ## Result Label (Initialized but cleared on subsequent submits)
        self.result_label = ctk.CTkLabel(self, text='')
        # Place label in the first column
        self.result_label.grid(row=11, column=0, padx=10, pady=10, sticky='W')

    
    def _create_input_row(self, label_text: str, row_index: int, attr_name: str):
        """
        A helper function to create and place a label and an entry widget in a single row.
        Attaches the CTkEntry widget to an instance variable for easy access.
        
        Args:
            label_text (str): The text for the CTkLabel.
            row_index (int): The row index in the grid.
            attr_name (str): The name to assign to the instance variable storing the CTkEntry.
        """
        # Create and place the Label in the first column
        label = ctk.CTkLabel(self, text=label_text)
        label.grid(row=row_index, column=0, padx=10, pady=10, sticky='W')
        
        # Create and place the Entry in the second column
        entry = ctk.CTkEntry(self)
        entry.grid(row=row_index, column=1, padx=10, pady=10, sticky='EW')
        
        # Set the entry object as an attribute on the class instance
        setattr(self, f'{attr_name}_entry', entry)


    def submit_prediction(self):
        """
        Gathers input data from the entry fields, calculates derived features,
        loads the machine learning model, and displays the prediction result.
        """
        # Dictionary to map the entry field attribute name to the model column name
        # The key is the attribute name set in _create_input_row (e.g., 'footfall_entry')
        # The value is the column name expected by the model (e.g., 'footfall')
        data_map = {
            'footfall': 'footfall',
            'tempMode': 'tempMode',
            'airQuality': 'AQ',
            'ultraSonicSensor': 'USS',
            'electricalCurrentReading': 'CS',
            'VOC': 'VOC',
            'RPM': 'RP', # Note: The original code used 'RP' for RPM in the DataFrame
            'InputPressure': 'IP',
            'Temperature': 'Temperature',
            'AverageRPM_Diff': 'RP_Avg'
        }
        
        try:
            # 1. Gather all raw input data
            raw_data = {}
            for key in data_map:
                # Get the CTkEntry object dynamically and call .get()
                entry_widget = getattr(self, f'{key}_entry')
                raw_data[key] = entry_widget.get()
            
            # Convert critical inputs to float for calculation
            current_temp = float(raw_data['Temperature'])
            mode_temp = float(raw_data['tempMode'])
            
            # 2. Calculate derived features
            # Calculate the difference between the measured Temperature and the set-point Temperature Mode
            temp_diff = current_temp - mode_temp
            
            # 3. Prepare data for the model (DataFrame creation)
            # Create a list of values in the order of the expected model columns
            model_input_data = [
                raw_data['footfall'], 
                raw_data['tempMode'],
                raw_data['airQuality'],
                raw_data['ultraSonicSensor'],
                raw_data['electricalCurrentReading'],
                raw_data['VOC'],
                raw_data['RPM'],
                raw_data['InputPressure'],
                raw_data['Temperature'],
                # Derived feature
                temp_diff, 
                raw_data['AverageRPM_Diff']
            ]
            
            # Define columns exactly as the trained model expects them
            model_columns = [
               'footfall', 'tempMode', 'AQ', 'USS', 'CS', 'VOC', 'RP', 'IP',
               'Temperature', 'temp_diff', 'RP_Avg'
            ]

            input_df = pd.DataFrame([model_input_data], columns=model_columns)
            
            # 4. Load Model and Predict
            # Use 'rb' (read binary) mode for pickle files
        
            if not os.path.exists(self.model_path):
                raise FileNotFoundError(f"Model file not found at: {self.model_path}")

            with open(self.model_path, 'rb') as file:
                model = pickle.load(file)
            
            # Make the prediction
            prediction = model.predict(input_df)
            
            # 5. Interpret Result
            if prediction[0] == 1:
                message = 'System Failure Imminent!'
                colour = 'red'
            elif prediction[0] == 0:
                message = 'System Operation is Normal.'
                colour = 'green'
        
        # --- Error Handling ---
        # Catch any exceptions during data retrieval, conversion, or prediction
        except FileNotFoundError as e:
            message = f'Model Error: {e}'
            colour = 'red'
        except ValueError:
            # Catches errors from float() conversion if fields are empty or non-numeric
            message = 'System Info Inconclusive. Check all inputs are numeric.'
            colour = 'orange'
        except Exception as e:
            # General catch-all for other errors (e.g., pickle load failure)
            message = f'An unexpected error occurred: {e}'
            colour = 'orange'
        
        # 6. Update the Result Label
        self.result_label.configure(text=f'Status: {message}', text_color=colour)
        
    
if __name__ == '__main__':
    # Get the directory of the currently running script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    MODEL_FILE_PATH = os.path.join(script_dir, 'model.pkl')
    app = MachineDetectApp(model_path=MODEL_FILE_PATH)
    app.mainloop()