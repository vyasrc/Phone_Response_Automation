import tkinter as tk
import os
import pandas as pd
from datetime import datetime


class GUI(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        master.title("Voice Message System")
        self.phone_info = []
        self.last_response = {}
        self.output_folder_name = 'Output Response Time.csv'
        self.create_widgets()

    def create_widgets(self):

        hs_label = tk.Label(text="Household ID")
        self.hs_txt = tk.Text(root, height=2, width=25, bg="light cyan")
        phn_label = tk.Label(text="Phone Number")
        self.phn_txt = tk.Text(root, height=2, width=25, bg="light cyan")
        self.phn_txt.insert(tk.END, '000-000-0000')
        call_time_label = tk.Label(text="Call Completed TimeStamp")
        self.call_time_txt = tk.Text(root, height=2, width=25, bg="light cyan")
        self.call_time_txt.insert(tk.END, 'MM/DD/YYYY HH:MM:SS')
        response_label = tk.Label(text="Response")
        self.response_txt = tk.Text(root, height=2, width=25, bg="light cyan")
        billing_info_label = tk.Label(text="Billing Duration (Seconds)")
        self.billing_info_txt = tk.Text(root, height=2, width=25, bg="light cyan")
        output_label = tk.Label(text="Output Folder Name")
        self.output_txt = tk.Text(root, height=2, width=25, bg="light cyan")
        self.output_txt.insert(tk.END, 'Output Response Time')

        hs_label.grid(column=0, row=0)
        self.hs_txt.grid(column=1, row=0)
        phn_label.grid(column=0, row=1)
        self.phn_txt.grid(column=1, row=1)
        call_time_label.grid(column=0, row=2)
        self.call_time_txt.grid(column=1, row=2)
        response_label.grid(column=0, row=3)
        self.response_txt.grid(column=1, row=3)
        billing_info_label.grid(column=0, row=4)
        self.billing_info_txt.grid(column=1, row=4)
        output_label.grid(column=0, row=5)
        self.output_txt.grid(column=1, row=5)

        display = tk.Button(root, height=2, width=20, text="Update", bg="light yellow", fg="red",
                            command=lambda: self.update_records())
        display.grid(column=2, row=2)
        quit_button = tk.Button(root, text="QUIT", fg="red", bg="light yellow",
                                width=20, height=2, command=root.destroy)
        quit_button.grid(column=2, row=3)

    def update_records(self):

        hs_input_info = self.hs_txt.get("1.0", "end-1c")
        phone_input_info = self.phn_txt.get("1.0", "end-1c")
        call_time_input_info = self.call_time_txt.get("1.0", "end-1c")
        call_time = datetime.strptime(call_time_input_info, "%m/%d/%Y %H:%M:%S")
        response_input_info = self.response_txt.get("1.0", "end-1c")
        bill_input_info = self.billing_info_txt.get("1.0", "end-1c")
        out_input_info = self.output_txt.get("1.0", "end-1c")
        # print(hs_input_info, int(phone_input_info.replace('-', '')), call_time_input_info, response_input_info,
        #       bill_input_info, round(int(bill_input_info)/60), out_input_info)
        self.phone_info.append({"Household ID": hs_input_info,
                                "Phone Number": int(phone_input_info.replace('-', '')),
                                "Call Completed TimeStamp": call_time,
                                "Response": response_input_info,
                                "Billing Duration In Seconds": int(bill_input_info),
                                "Billing Duration In Minutes": round(int(bill_input_info)/60)})

        self.hs_txt.delete("1.0", "end-1c")
        self.phn_txt.delete("1.0", "end-1c")
        self.call_time_txt.delete("1.0", "end-1c")
        self.phn_txt.insert(tk.END, '000-000-0000')
        self.call_time_txt.insert(tk.END, 'MM/DD/YYYY HH:MM:SS')
        self.response_txt.delete("1.0", "end-1c")
        self.billing_info_txt.delete("1.0", "end-1c")

        if self.phone_info:
            # print(self.phone_info[-1])
            record = self.phone_info[-1]
            if 'Disconnected' in record['Response']:
                filename = 'Disconnected Numbers/' + str(record['Phone Number']) + '.csv'
                if not os.path.exists(os.path.dirname(filename)):
                    os.makedirs(os.path.dirname(filename))
                df = pd.DataFrame(record.items())
                df.transpose().to_csv(filename, index=False, header=False)

            if record['Response'] == 'Answering Machine':
                if record['Household ID'] not in self.last_response.keys():
                    self.last_response[record['Household ID']] = [{'Phone No:': record['Phone Number'],
                                                                   'Last Response Time': call_time}]
                else:
                    in_flag = False
                    for phone_record in self.last_response[record['Household ID']]:
                        if phone_record['Phone No:'] == record['Phone Number']:
                            # print(call_time, phone_record['Last Response Time'])
                            if call_time > phone_record['Last Response Time']:
                                phone_record['Last Response Time'] = call_time
                            in_flag = True
                    if not in_flag:
                        self.last_response[record['Household ID']].append({'Phone No:': record['Phone Number'],
                                                                           'Last Response Time': call_time})
            self.write_output(out_input_info)

    def write_output(self, output_name):

        saved_time = None
        output = {}
        # print(self.last_response)
        if not os.path.exists(self.output_folder_name):
            self.output_folder_name = output_name + '.csv'
            for household in self.last_response.keys():
                latest_time = datetime.min
                for phone in self.last_response[household]:
                    if phone['Last Response Time'] > latest_time:
                        latest_time = phone['Last Response Time']
                output[household] = latest_time
        else:
            if self.output_folder_name != output_name + '.csv':
                os.rename(self.output_folder_name, output_name + '.csv')
                self.output_folder_name = output_name + '.csv'
            temp_output = pd.read_csv(self.output_folder_name).to_dict('records')
            # print(temp_output)

            for household in self.last_response.keys():
                latest_time = datetime.min
                for phone in self.last_response[household]:
                    if phone['Last Response Time'] > latest_time:
                        latest_time = phone['Last Response Time']
                # print(type(temp_output))
                for record in temp_output:
                    if str(record['Household ID']) == household:
                        saved_time = datetime.strptime(record['Last Response Time'],
                                                       "%Y-%m-%d %H:%M:%S")
                        if latest_time > saved_time:
                            saved_time = latest_time
                            break
                output[household] = saved_time
        df = pd.DataFrame(output.items(), columns=['Household ID', 'Last Response Time'])
        df.to_csv(self.output_folder_name, index=False)


root = tk.Tk()
app = GUI(master=root)
app.mainloop()
