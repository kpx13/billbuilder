#!/usr/bin/python
# -*- coding: utf-8 -*-

f = open('reports/profiling/handlers', 'r')
f_out = open('reports/profiling/handlers_report', 'w')

calls = {}
for l in f.readlines():
    tmp = l.strip().split(' ')
    module_name = tmp[0]
    curr_time = float(tmp[-1])
    if module_name in calls:
        calls[module_name] = calls[module_name] + [curr_time]
    else:
        calls[module_name] = [curr_time]


result = []        
for k, v in calls.iteritems():
    sum_time = sum(v)
    num_calls = len(v)
    mid_time = sum_time / num_calls
    # кортеж: название ф-ции, общее время, кол-во вызывов, среднее время
    result.append((k, sum_time, num_calls, mid_time))
    
# сортируем по времени отработки
result.sort(key=lambda sum_time: -sum_time[1])

num_result = 0
sum_result = 0

for r in result:
    print '%24s%16.3f%4d%16.3f' % r
    f_out.write('%24s%16.3f%8d%16.3f\n' % r)
    num_result += 1
    sum_result += r[3]
    
mid_result = sum_result / num_result
    
print '----------------------------'
print '%36s%8d%16.3f\n' % (' ', num_result, mid_result)
f_out.write('----------------------------\n' )
f_out.write('%36s%8d%16.3f\n' % (' ', num_result, mid_result))



