import matplotlib.pyplot as plt
import sys
import argparse
import re


class Report:
    def __init__(self, _in, _out, _unit, _interface, _date=None):
        if _date is not None:
            self.date = _date

        if _in is not None and _out is not None and _unit is not None and _interface is not None:
            self.inbw = _in
            self.outbw = _out
            self.unit = _unit
            self.interface = _interface

    def getIn(self):
        if self.inbw is not None:
            return self.inbw

    def getOut(self):
        if self.outbw is not None:
            return self.outbw

    def getUnit(self):
        if self.unit is not None:
            return self.unit

    def getInterface(self):
        if self.interface is not None:
            return self.interface

    def getDate(self):
        if self.date is not None:
            return self.date

    def __repr__(self):
        return "['in':'{}', 'out':'{}', 'unit':'{}', 'interface':'{}', 'date':'{}']".format(self.getIn(),
                                                                                            self.getOut(),
                                                                                            self.getUnit(),
                                                                                            self.getInterface(),
                                                                                            self.getDate())

    def __str__(self):
        return '@{}, on interface {}, {} {} in, {} {} out'.format(self.getDate(),
                                                                  self.getInterface(),
                                                                  self.getIn(),
                                                                  self.getUnit(),
                                                                  self.getOut(),
                                                                  self.getUnit())


def ema(data, window):
    if len(data) < window + 2:
        return None
    alpha = 2 / float(window + 1)
    ema = []
    for i in range(0, window):
        ema.append(None)
    ema.append(data[window])
    for i in range(window+1, len(data)):
        ema.append(ema[i-1] + alpha*(data[i]-ema[i-1]))
    return ema


def chart(args, data):
    # Setting the default values
    ema_window = 60
    if args.ema is not None:
        ema_window = int(args.ema)

    for key in data:
        interface = data[key]
        debit_in = []
        debit_out = []
        date = []
        for report in interface:
            debit_in.append(float(report.getIn()))
            debit_out.append(float(report.getOut()))
            date.append(report.getDate())
        plt.plot(debit_in, label='In bandwidth', data=date)
        plt.plot(debit_out, label='Out bandwidth', data=date)
        plt.plot(ema(debit_in, ema_window), label='Bandwidth {} period moving average'.format(ema_window), color='m')
        plt.axhline(sum(debit_in)/len(debit_in), label='Average in bandwidth', color='g')
        plt.axhline(sum(debit_out)/len(debit_out), label='Average out bandwidth', color='r')
        plt.legend()
        if args.log:
            plt.yscale('log')
        else:
            plt.ylim(bottom=0)
            plt.yscale('linear')
        plt.ylabel(interface[0].getUnit())
        plt.xlabel('time')
        plt.show()


def clean_whitespace(data):
    new_data = []
    for line in data:
        new_line = re.sub('\n', '', line)
        new_data.append(re.sub(' +', ' ', new_line).split(' '))
    return new_data


def parse_unit(data):
    for line in data:
        # If it is the header time and unit line
        if line[0] == 'HH:MM:SS':
            return line[1]


def parse_interfaces(data):
    interfaces = []
    for line in data:
        # If it is the TIME INT1 INT2 line ...
        if line[1] == 'Time':
            for i in range(2, len(line) - 1):
                interfaces.append(line[i])
            return interfaces


def clean_data(data):
    cleaned_data = []
    for line in data:
        if line[1] != 'Time' and line[0] != 'HH:MM:SS':
            cleaned_data.append(line)
    return cleaned_data


def parse(args, file_data):
    raw_data = clean_whitespace(file_data)
    unit = parse_unit(raw_data)
    interfaces = parse_interfaces(raw_data)
    cleaned_data = clean_data(raw_data)

    arranged_data = dict()
    for interface in interfaces:
        arranged_data[interface] = []

    for line in cleaned_data:
        for i in range(0, len(interfaces)):
            arranged_data[interfaces[i]].append(Report(line[(i*2)+1], line[(i*2)+2], unit, interfaces[i], line[0]))

    return arranged_data


def be_verbose(file_data):
    pass


def main(argv):
    parser = argparse.ArgumentParser(description='A python script that can be used to have a nice display of a ifstat output.', epilog="Note: ifstat must be used with -t for this script to work")
    parser.add_argument('input', nargs='?', help='Output file from ifstat')
    parser.add_argument('-a', '--ema', help='Exponential moving average used to smooth the bandwidth. Default at 60.', type=int)
    parser.add_argument('-v', '--verbose', help='Increase output verbosity', action='store_true')
    parser.add_argument('-l', '--log', help='Plot will be in logarithmic scale', action='store_true')
    args = parser.parse_args(argv)
    with open(args.input) as f:
        file_data = f.readlines()
        if args.verbose:
            be_verbose(file_data)
        parsed_data = parse(args, file_data)
        chart(args, parsed_data)


if __name__ == "__main__":
    main(sys.argv[1:])
