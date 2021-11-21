import pandas as pd
from datetime import datetime
import os

class AnsweringMachine:

    def __init__(self):
        self.phone_input = pd.read_csv('Sample Phone#Input.csv')
        self.vm_input = pd.read_csv('Sample VMInput.csv')
        self.last_response = {}

    def last_response_am(self):

        response_time = None

        for index, row in self.phone_input.iterrows():
            if row['Phone Number'] in list(self.vm_input['PhoneNumberDialed']):
                vm_row = self.vm_input.loc[self.vm_input['PhoneNumberDialed'] == row['Phone Number']]
                for index2, row2 in vm_row.iterrows():
                    if row2['Response'] == 'Answering_Machine':
                        if '/' in row2['CallCompletedTimeStamp']:
                            response_time = pd.to_datetime(row2['CallCompletedTimeStamp'],
                                                           format="%m/%d/%Y %H:%M")
                        elif '.' in row2['CallCompletedTimeStamp']:
                            response_time = pd.to_datetime(row2['CallCompletedTimeStamp'],
                                                           format="%m.%d.%Y %H:%M")
                        if row['Household ID'] not in self.last_response.keys():
                            self.last_response[row['Household ID']] = [{'Phone No:': row['Phone Number'],
                                                                       'Last Response Time': response_time}]
                        else:
                            in_flag = False
                            for record in self.last_response[row['Household ID']]:
                                if record['Phone No:'] == row['Phone Number']:
                                    record['Last Response Time'] = response_time
                                    in_flag = True
                                    break
                            if not in_flag:
                                self.last_response[row['Household ID']].append({'Phone No:': row['Phone Number'],
                                                                                'Last Response Time': response_time})

    def write_output(self):

        output = {}
        for household in self.last_response.keys():
            latest_time = datetime.min
            for phone in self.last_response[household]:
                if phone['Last Response Time'] > latest_time:
                    latest_time = phone['Last Response Time']
            output[household] = latest_time
        df = pd.DataFrame(output.items(), columns=['Household ID', 'Last Response Time'])
        df.to_csv('Output Response Time.csv', index=False)

    def disconnected_phone_check(self):

        for index, row in self.vm_input.iterrows():
            if 'Disconnected' in row['Response']:
                filename = 'Disconnected Numbers/' + str(row['PhoneNumberDialed']) + '.csv'
                if not os.path.exists(os.path.dirname(filename)):
                    os.makedirs(os.path.dirname(filename))
                df = pd.DataFrame(row.to_dict().items())
                df.transpose().to_csv(filename, index=False, header=False)


obj = AnsweringMachine()
obj.last_response_am()
obj.write_output()
obj.disconnected_phone_check()
