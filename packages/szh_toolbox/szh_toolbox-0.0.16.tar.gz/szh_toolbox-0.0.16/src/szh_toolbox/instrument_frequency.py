class FrequencyChannel:
    QH = 1
    QV = 2

    def __init__(self, chid, frequency_list: list, polarization):
        self.chid = chid
        self.frequency_list = frequency_list
        self.polarization = polarization
        self.autofit()

    def autofit(self):
        self.all_frequencies = self.compute_all_frequency_point(self.frequency_list)
        self.max_frequency = max(self.all_frequencies)
        self.min_frequency = min(self.all_frequencies)
        self.frequency = self.frequency_list[0]
        self.fre_str = "±".join(map(str, self.frequency_list)) + 'GHz'

    def compute_all_frequency_point(self, frequency_list):
        res = []
        a = frequency_list
        if len(a) == 0:
            return []
        elif len(a) == 1:
            res.append(a[0])
        elif len(a) == 2:
            res.append(a[0]+a[1])
            res.append(a[0]-a[1])
        elif len(a) == 3:
            res.append(a[0]+a[1]+a[2])
            res.append(a[0]+a[1]-a[2])
            res.append(a[0]-a[1]+a[2])
            res.append(a[0]-a[1]-a[2])
        else:
            raise Exception("Not support")

        return res

    def __repr__(self) -> str:
        str_numbers = list(map(str, self.frequency_list))
        fre_str = "±".join(str_numbers)
        id_str = f'CH{self.chid}:'
        pol_str = 'QH' if self.polarization == FrequencyChannel.QH else 'QV'
        return f'{id_str:<5} {fre_str}GHz {pol_str}'


class InstrumentFrequencyModel:
    def __init__(self, name):
        self.name = name
        self.channels = []

    def add_channel(self, *args, **kwargs):
        self.channels.append(FrequencyChannel(*args, **kwargs))

    def get_channel(self, chid) -> FrequencyChannel:
        if chid > 0 and chid <= len(self.channels):
            return self.channels[chid-1]
        else:
            raise Exception(f'通道编号: {chid} 超出了范围')

    def __repr__(self) -> str:
        res = []
        res.append(f"{self.name}有以下频道：")
        for channel in self.channels:
            res.append(f'{channel}')

        return '\n'.join(res)


class ATMSFrequency(InstrumentFrequencyModel):
    def __init__(self):
        super().__init__('ATMS')
        QH = FrequencyChannel.QH
        QV = FrequencyChannel.QV
        f0 = 57.290344
        self.add_channel(1,  [23.8],  QV)
        self.add_channel(2,  [31.4],  QV)
        self.add_channel(3,  [50.3],  QH)
        self.add_channel(4,  [51.76], QH)
        self.add_channel(5,  [52.8],  QH)
        self.add_channel(6,  [53.596, 0.115], QH)
        self.add_channel(7,  [54.4],  QH)
        self.add_channel(8,  [54.94], QH)
        self.add_channel(9,  [55.5],  QH)
        self.add_channel(10, [f0], QH)
        self.add_channel(11, [f0, 0.217], QH)
        self.add_channel(12, [f0, 0.3222, 0.048],  QH)
        self.add_channel(13, [f0, 0.3222, 0.022],  QH)
        self.add_channel(14, [f0, 0.3222, 0.010],  QH)
        self.add_channel(15, [f0, 0.3222, 0.0045], QH)
        self.add_channel(16, [88.2],  QV)
        self.add_channel(17, [165.5], QH)
        self.add_channel(18, [183.31, 7.0], QH)
        self.add_channel(19, [183.31, 4.5], QH)
        self.add_channel(20, [183.31, 3.0], QH)
        self.add_channel(21, [183.31, 1.8], QH)
        self.add_channel(22, [183.31, 1.0], QH)


class GMSSFrequency(InstrumentFrequencyModel):
    def __init__(self):
        super().__init__('GMSS')
        QH = FrequencyChannel.QH
        QV = FrequencyChannel.QV
        f0 = 57.290344
        self.add_channel(1,  [23.8], QV)
        self.add_channel(2,  [23.8], QH)
        self.add_channel(3,  [31.4], QV)
        self.add_channel(4,  [31.4], QH)
        self.add_channel(5,  [50.3], QV)
        self.add_channel(6,  [50.3], QH)
        self.add_channel(7,  [51.76], QH)
        self.add_channel(8,  [52.8], QH)
        self.add_channel(9,  [53.246, 0.08], QH)
        self.add_channel(10, [53.596, 0.115], QH)
        self.add_channel(11, [53.948, 0.081], QH)
        self.add_channel(12, [54.4], QH)
        self.add_channel(13, [54.94], QH)
        self.add_channel(14, [55.5], QH)
        self.add_channel(15, [f0], QH)
        self.add_channel(16, [f0, 0.217], QH)
        self.add_channel(17, [f0, 0.322, 0.048], QH)
        self.add_channel(18, [f0, 0.322, 0.022], QH)
        self.add_channel(19, [f0, 0.322, 0.01], QH)
        self.add_channel(20, [f0, 0.322, 0.0045], QH)
        self.add_channel(21, [89], QV)
        self.add_channel(22, [118.75, 0.08], QH)
        self.add_channel(23, [118.75, 0.2], QH)
        self.add_channel(24, [118.75, 0.3], QH)
        self.add_channel(25, [118.75, 0.8], QH)
        self.add_channel(26, [118.75, 1.1], QH)
        self.add_channel(27, [118.75, 2.5], QH)
        self.add_channel(28, [118.75, 3.0], QH)
        self.add_channel(29, [118.75, 5.0], QH)
        self.add_channel(30, [165.5], QV)
        self.add_channel(31, [183.31, 11], QH)
        self.add_channel(32, [183.31, 7.0], QH)
        self.add_channel(33, [183.31, 4.5], QH)
        self.add_channel(34, [183.31, 3.0], QH)
        self.add_channel(35, [183.31, 1.8], QH)
        self.add_channel(36, [183.31, 1.0], QH)
        self.add_channel(37, [229], QV)
        self.add_channel(38, [380.197, 18.0], QH)
        self.add_channel(39, [380.197, 9.0], QH)
        self.add_channel(40, [380.197, 1.5], QH)
        self.add_channel(41, [380.197, 0.4], QH)
        self.add_channel(42, [424.763, 4.0], QH)
        self.add_channel(43, [424.763, 1.5], QH)
        self.add_channel(44, [424.763, 1.0], QH)
        self.add_channel(45, [424.763, 0.6], QH)
        self.add_channel(46, [424.763, 0.3], QH)


class CCMSFrequency(InstrumentFrequencyModel):
    def __init__(self):
        super().__init__('GMSS')
        QH = FrequencyChannel.QH
        QV = FrequencyChannel.QV
        f0 = 57.290344
        self.add_channel(1, [50.3], QV)
        self.add_channel(2, [50.3], QH)
        self.add_channel(3, [51.76], QH)
        self.add_channel(4, [52.8], QH)
        self.add_channel(5, [53.246, 0.08], QH)
        self.add_channel(6, [53.596, 0.115], QH)
        self.add_channel(7, [53.948, 0.081], QH)
        self.add_channel(8, [54.4], QH)
        self.add_channel(9, [54.94], QH)
        self.add_channel(10, [55.5], QH)
        self.add_channel(11, [f0], QH)
        self.add_channel(12, [f0, 0.217], QH)
        self.add_channel(13, [f0, 0.322, 0.048], QH)
        self.add_channel(14, [f0, 0.322, 0.022], QH)
        self.add_channel(15, [f0, 0.322, 0.01], QH)
        self.add_channel(16, [f0, 0.322, 0.0045], QH)
        self.add_channel(17, [89], QV)
        self.add_channel(18, [118.75, 0.08], QH)
        self.add_channel(19, [118.75, 0.2], QH)
        self.add_channel(20, [118.75, 0.3], QH)
        self.add_channel(21, [118.75, 0.8], QH)
        self.add_channel(22, [118.75, 1.1], QH)
        self.add_channel(23, [118.75, 2.5], QH)
        self.add_channel(24, [118.75, 3.0], QH)
        self.add_channel(25, [118.75, 5.0], QH)
        self.add_channel(26, [165.5], QV)
        self.add_channel(27, [183.31, 11], QH)
        self.add_channel(28, [183.31, 7.0], QH)
        self.add_channel(29, [183.31, 4.5], QH)
        self.add_channel(30, [183.31, 3.0], QH)
        self.add_channel(31, [183.31, 1.8], QH)
        self.add_channel(32, [183.31, 1.0], QH)


if __name__ == "__main__":
    fm = ATMSFrequency()
    fm.get_channel(12).fre_str
