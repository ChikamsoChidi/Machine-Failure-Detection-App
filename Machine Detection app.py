import customtkinter as ctk
import pandas as pd
import pickle

ctk.set_appearance_mode('light')

ctk.set_default_color_theme('blue')

class MachineDetectApp(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        
        self.title('Machine Failure Detection App')
        self.geometry('420x530')
        
        self.footfallLabel = ctk.CTkLabel(self, text = 'Foot fall')
        self.footfallLabel.grid(row = 1, column = 1, padx = 10, pady = 10)
        self.footfallEntry = ctk.CTkEntry(self)
        self.footfallEntry.grid(row = 1, column = 2)
        
        self.tempModeLabel = ctk.CTkLabel(self, text = 'Temperature Mode')
        self.tempModeLabel.grid(row = 2, column = 1, padx = 10, pady = 10)
        self.tempModeEntry = ctk.CTkEntry(self)
        self.tempModeEntry.grid(row = 2, column = 2)
        
        self.airQualityLabel = ctk.CTkLabel(self, text = 'Air Quality')
        self.airQualityLabel.grid(row = 3, column = 1, padx = 10, pady = 10)
        self.airQualityEntry = ctk.CTkEntry(self)
        self.airQualityEntry.grid(row = 3, column = 2)
        
        
        self.ultraSonicSensorLabel = ctk.CTkLabel(self, text = 'UltraSonic Sensor reading')
        self.ultraSonicSensorLabel.grid(row = 4, column = 1, padx = 10, pady = 10)
        self.ultraSonicSensorEntry = ctk.CTkEntry(self)
        self.ultraSonicSensorEntry.grid(row = 4, column = 2)
        
        self.electricalCurrentReadingLabel = ctk.CTkLabel(self, text = 'Electric Current')
        self.electricalCurrentReadingLabel.grid(row = 5, column = 1, padx = 10, pady = 10)
        self.electricalCurrentReadingEntry = ctk.CTkEntry(self)
        self.electricalCurrentReadingEntry.grid(row = 5, column = 2)
        
        self.VOCLabel = ctk.CTkLabel(self, text = 'Volatile Organic Compound Levels')
        self.VOCLabel.grid(row = 6, column = 1, padx = 10, pady = 10)
        self.VOCEntry = ctk.CTkEntry(self)
        self.VOCEntry.grid(row = 6, column = 2)
        
        self.RPMLabel = ctk.CTkLabel(self, text = 'Rotations Per Minute')
        self.RPMLabel.grid(row = 7, column = 1, padx = 10, pady = 10)
        self.RPMEntry = ctk.CTkEntry(self)
        self.RPMEntry.grid(row = 7, column = 2)
        
        self.InputPressureLabel = ctk.CTkLabel(self, text = 'Input Pressure')
        self.InputPressureLabel.grid(row = 8, column = 1, padx = 10, pady = 10)
        self.InputPressureEntry = ctk.CTkEntry(self)
        self.InputPressureEntry.grid(row = 8, column = 2)

        self.TemperatureLabel = ctk.CTkLabel(self, text = 'Temperature')
        self.TemperatureLabel.grid(row = 9, column = 1, padx = 10, pady = 10)
        self.TemperatureEntry = ctk.CTkEntry(self)
        self.TemperatureEntry.grid(row = 9, column = 2)
        
        self.AverageRPM_DiffLabel = ctk.CTkLabel(self, text = 'Average RPM Difference')
        self.AverageRPM_DiffLabel.grid(row = 10, column = 1, padx = 10, pady = 10)
        self.AverageRPM_DiffEntry = ctk.CTkEntry(self)
        self.AverageRPM_DiffEntry.grid(row = 10, column = 2)
        
        
        self.SubmitButton = ctk.CTkButton(self, text = 'Submit', command = self.Submit)
        self.SubmitButton.grid(row = 11, column = 2, padx = 20, pady = 10)
        
        

        
    def Submit (self):
        try:
            footfall = self.footfallEntry.get() 
            tempMode = self.tempModeEntry.get()
            airQuality = self.airQualityEntry.get()
            ultraSonicSensor = self.ultraSonicSensorEntry.get()
            electricalCurrentReading = self.electricalCurrentReadingEntry.get()
            VOC = self.VOCEntry.get()
            RPM = self.RPMEntry.get()
            InputPressure = self.InputPressureEntry.get()
            Temperature = self.TemperatureEntry.get()
            
            Avg_RPM_Diff = self.AverageRPM_DiffEntry.get()
            temp_diff = float(Temperature)-float(tempMode)
            array = pd.DataFrame(
            [[footfall, 
              tempMode,
              airQuality,
              ultraSonicSensor,
              electricalCurrentReading,
              VOC,
              RPM,
              InputPressure,
              Temperature,
              temp_diff,
              Avg_RPM_Diff]],
            columns = ['footfall',
               'tempMode', 
               'AQ', 
               'USS', 
               'CS', 
               'VOC', 
               'RP', 
               'IP',
             'Temperature', 
             'temp_diff', 
             'RP_Avg'])
                
            
            with open(r"C:\Users\OWNER\Desktop\Tech IT\Machine Failure Detect\model.pkl", 'rb') as file:
                model = pickle.load(file)
            
            result = model.predict(array)
            if result[0] == 1:
                message = 'System Failure Imminent!'
                colour = 'red'
            elif result[0] == 0:
                message = 'System Operation is Normal.'
                colour = 'green'
        except:
            message = 'System Info Inconclusive.'
            colour = 'orange'
        self.SubmitResult = ctk.CTkLabel(self, text = '')
        self.SubmitResult = ctk.CTkLabel(self, text = f'Status: {message}', text_color=colour)
        self.SubmitResult.grid(row = 11, column = 1)
        
    
if __name__ == '__main__':
    app = MachineDetectApp()
    app.mainloop()