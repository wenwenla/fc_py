

class Log:

    def __init__(self):
        self.lines = []
        with open('log.txt', 'r') as fin:
            for line in fin:
                line = line.split()
                last = line[-7:]
                status = {
                    'PC': int(line[0], 16),
                    'A': int(last[0][2:], 16),
                    'X': int(last[1][2:], 16),
                    'Y': int(last[2][2:], 16),
                    'F': int(last[3][2:], 16),
                    'SP': int(last[4][3:], 16),
                    'CYC': int(last[6][4:])
                }
                self.lines.append(status)
        self.now_pos = 0

    def check(self, log):
        for k, v in log.items():
            if self.lines[self.now_pos][k] != v:
                return False
        return True

    def log(self):
        return self.lines[self.now_pos]

    def next(self):
        self.now_pos += 1
        return self.now_pos == len(self.lines)
