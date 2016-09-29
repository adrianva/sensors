
class ChartData(object):
    @classmethod
    def convert_data_to_json(cls, signals):
        data = {'dates': []}
        for signal in signals:
            data['dates'].append(signal.date.strftime('%m-%d'))

            if signal.signal_id not in data:
                data[signal.signal_id] = []
                data['signal'] = signal.signal_id

            data[signal.signal_id].append(signal.value)

        return data
