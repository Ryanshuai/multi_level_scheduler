from collections import defaultdict


class Thread:
    def __init__(self, name, need_time, arrive_time):
        self.name = name
        self.need_time = need_time
        self.arrive_time = arrive_time
        self.running_time = need_time
        self.start_time = -1
        self.end_time = -1

    def run(self, t, can_run_time, level):
        if level == 0:
            self.start_time = t

        run_time = min(self.need_time, can_run_time)
        self.need_time -= run_time
        if self.need_time == 0:
            self.end_time = t + run_time

        print("{} runs {} -> {} \t at L{} \t remain {}->{}".format(self.name, t, t + run_time, level + 1,
                                                                   self.need_time + run_time,
                                                                   self.need_time))
        return run_time


class Scheduler:
    def __init__(self, level_times, thread_queue):
        self.time = 0
        self.level_times = level_times
        self.thread_queue = thread_queue
        self.level_queues = defaultdict(list)

    def any_queue_remain(self):
        for level in self.level_queues:
            if self.level_queues[level]:
                return level
        return -1

    def run(self):
        while self.any_queue_remain() != -1 or self.thread_queue:
            if self.any_queue_remain() == -1 and self.thread_queue[0].arrive_time > self.time:
                self.time += 1
                continue

            while self.thread_queue and self.thread_queue[0].arrive_time <= self.time:
                thread = self.thread_queue.pop(0)
                self.level_queues[0].append(thread)

            # print("time={}".format(self.time) + "-" * 50)
            # for [level, queue] in self.level_queues.items():
            #     print("L{}: \t".format(level), end="")
            #     [print("{}({})".format(thread.name, thread.need_time), end=" ") for thread in queue]
            #     print("")

            running_level = self.any_queue_remain()
            running_thread = self.level_queues[running_level].pop(0)
            self.time += running_thread.run(self.time, self.level_times[running_level], running_level)
            new_running_level = min(running_level + 1, len(self.level_times) - 1)
            if running_thread.need_time:
                self.level_queues[new_running_level].append(running_thread)


if __name__ == '__main__':
    # winter 2022 hw2
    p1 = Thread("p1", 18, 0)
    p2 = Thread("p2", 4, 5)
    p3 = Thread("p3", 2, 10)
    p4 = Thread("p4", 5, 15)
    p5 = Thread("p5", 10, 20)

    scheduler = Scheduler([1, 3, 5], [p1, p2, p3, p4, p5])
    scheduler.run()
    print("process\t arrive\t finish\t running\t normalized_turnaround")
    for p in [p1, p2, p3, p4, p5]:
        print("{}\t{}\t{}\t{}\t{}".format(p.name, p.arrive_time, p.end_time, p.running_time,
                                          (p.end_time - p.arrive_time) / p.running_time))

    # # summer 2021 hw2
    # p1 = Thread("p1", 20, 0)
    # p2 = Thread("p2", 5, 5)
    # p3 = Thread("p3", 2, 10)
    # p4 = Thread("p4", 4, 15)
    # p5 = Thread("p5", 12, 20)
    #
    # scheduler = Scheduler([2, 4, 6], [p1, p2, p3, p4, p5])
    # scheduler.run()

    # # CS153 Fall 16
    # p1 = Thread("p1", 10, 0)
    # p2 = Thread("p2", 2, 2)
    # p3 = Thread("p3", 1, 4)
    # p4 = Thread("p4", 8, 6)
    # p5 = Thread("p5", 4, 8)
    #
    # scheduler = Scheduler([1, 2, 4], [p1, p2, p3, p4, p5])
    # scheduler.run()

    # # CS153 Fall 17
    # p1 = Thread("p1", 17, 0)
    # p2 = Thread("p2", 5, 5)
    # p3 = Thread("p3", 1, 10)
    # p4 = Thread("p4", 11, 15)
    # p5 = Thread("p5", 8, 20)
    #
    # scheduler = Scheduler([1, 8], [p1, p2, p3, p4, p5])
    # scheduler.run()

    # # CS153 Winter 15
    # p1 = Thread("p1", 8, arrive_time=0)
    # p2 = Thread("p2", 2, arrive_time=0)
    # p3 = Thread("p3", 1, arrive_time=0)
    # p4 = Thread("p4", 3, arrive_time=0)
    # p5 = Thread("p5", 10, arrive_time=0)
    # p6 = Thread("p6", 4, arrive_time=0)
    #
    # scheduler = Scheduler([1, 2, 4], [p1, p2, p3, p4, p5, p6])
    # scheduler.run()
