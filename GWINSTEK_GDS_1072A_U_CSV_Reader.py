import numpy as np
from matplotlib import pyplot as plt


class GWINSTEK_GDS_1072A_U_CSV_Reader:
    parsed_data = []

    def parse_data(self, fds):
        if not isinstance(fds, list):
            raise TypeError(
                'The file descriptors must be given in a list. In case of a ' +
                'single file descriptor input it as ["your_data_file.csv"].'
            )
        for idx, fd in enumerate(fds):
            file_data = {}
            waveform_data_flag = False
            with open(fd, 'r') as file:
                for line in file:
                    line_data = line.rstrip(',\n').rsplit(',')
                    if line_data[0] in [
                        'Memory Length', 'Trigger Level', 'Vertical Scale',
                        'Vertical Position', 'Horizontal Scale',
                        'Horizontal Position', 'Sampling Period'
                        ]:
                        line_data[1] = float(line_data[1])
                    if (line_data[0] != 'Waveform Data'
                        and waveform_data_flag is False):
                        file_data.update({line_data[0]: line_data[1]})
                    elif waveform_data_flag is False:
                        file_data.update({line_data[0]: [[],[]]})
                        waveform_data_flag = True
                    else:
                        file_data['Waveform Data'][0].append(
                            float(line_data[0])
                            )
                        if idx:
                            file_data['Waveform Data'][1].append(
                                float(line_data[1])
                                )
                        else:
                            file_data['Waveform Data'][1].append(
                                float(line_data[1])
                                )
            self.parsed_data.append(file_data)
    
    def plot_data(self, as_captured=True, show_metadata=True):
        legend_entries = []
        metadata_pos = [
            (0.01, 0.01, 'left', 'bottom'),
            (0.99, 0.01, 'right', 'bottom')
        ]
        _, ax = plt.subplots()
        for idx, file_data in enumerate(self.parsed_data):
            if as_captured:
                file_data['Waveform Data'][1] = [
                    y+file_data['Vertical Position']
                    for y in file_data['Waveform Data'][1]
                ]
            else:
                file_data['Waveform Data'][0] = [
                    x+file_data['Horizontal Position']
                    for x in file_data['Waveform Data'][0]
                ]
            plt.plot(
                file_data['Waveform Data'][0],
                file_data['Waveform Data'][1]
                )
            legend_entries.append(file_data['Source'])
            if show_metadata:
                plt.text(
                    metadata_pos[idx][0], metadata_pos[idx][1],
                    f'{file_data["Source"]}\n' +
                    f'------\n' +
                    f'Memory Length: {file_data["Memory Length"]}\n' +
                    f'Trigger Level: {file_data["Trigger Level"]}\n' +
                    f'Sampling Period: {file_data["Sampling Period"]}\n' +
                    f'Probe: {file_data["Probe"]}\n' +
                    f'Horizontal Mode: {file_data["Horizontal Mode"]}\n' +
                    f'Mode: {file_data["Mode"]}\n' +
                    f'Time: {file_data["Time"]}\n' +
                    f'Firmware: {file_data["Firmware"]}',
                    color='black',
                    ha=metadata_pos[idx][2],
                    va=metadata_pos[idx][3],
                    transform=ax.transAxes
                )
        plt.xlabel(f'[{self.parsed_data[0]["Horizontal Units"]}]')
        plt.ylabel(f'[{self.parsed_data[0]["Vertical Units"]}]')
        plt.legend(legend_entries)
        plt.tight_layout()
        plt.show()
