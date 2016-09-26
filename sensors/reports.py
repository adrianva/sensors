
class ChartData(object):
    @classmethod
    def convert_data_to_json(cls, signals):
        data = {'dates': []}
        for signal in signals:
            data['dates'].append(signal.date.strftime('%m-%d'))

            if not data.has_key(signal.signal_id):
                data[signal.signal_id] = []
                data['signal'] = signal.signal_id

            data[signal.signal_id].append(signal.value)

        return data
