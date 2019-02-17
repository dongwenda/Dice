# -*- coding: utf-8 -*-
__author__ = 'dongwenda'
__date__ = '2019/2/17 17:46'

from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View

def index(request):
    return render(request, 'demo.html')


def demo(request):
    content = {}
    content['c'] = ''

    my_dice = request.GET.get('my_dice', '12345')
    num = request.GET.get('num', '230')
    print(type(my_dice),type(num))

    my_dices = [int(i) for i in my_dice]

    # 所有骰子组合的列表
    dice_list = [
        [one, two, three, four, fire]
        for one in range(1, 7)
        for two in range(1, 7)
        for three in range(1, 7)
        for four in range(1, 7)
        for fire in range(1, 7)
    ]
    # print(dice_list)

    # 所有的骰子的组合数
    all_dice = len(dice_list)

    def count_dice_num(count_num_list, num_list):
        count_num = 0
        for num in count_num_list:
            count_num += num_list.count(num)
        return count_num

    # t = [2, 1, 2, 3, 6, 3]
    # print(float(count_dice_num([2,1],t)))
    # print(float(1)/float(3))

    def probability(times, number, is_only=False):
        n = 0
        if is_only:
            for num_list in dice_list:
                if count_dice_num({number}, num_list) >= times:
                    n += 1
        else:
            for num_list in dice_list:
                if count_dice_num({1, number}, num_list) >= times:
                    n += 1
        return n / all_dice

    # for times in range(1,6):
    #     for num in range(1,7):
    #         print('{}个{}概率为：{}%'.format(times,num,round(probability(times,num,is_only=False)*100, 4)))



    def get_times_num_probability(times, num, is_only=False):

        def p_count(times, num_, is_only):
            actual_times = times - my_dices.count(num_)
            p = round(probability(actual_times, num_, is_only) * 100, 4)
            return p

        my_dices_set = set(my_dices)

        only = "斋" if is_only else "不斋"
        s = '你当前的骰子为：%s\n' %my_dices
        content['c'] += s
        content['c'] += '对方叫 {}个{} {}，概率为：{}%\n'.format(times, num, only, p_count(times, num, is_only))
        content['c'] += '=================================\n'
        content['c'] += '不斋：\n'
        # 展示当前叫的个数，我当前持有的骰数的，不斋概率
        content['c'] += '不+1\n'
        for my_num in my_dices_set:
            if my_num > num:
                content['c'] += '-->{}个{}不斋的概率:{}%\n'.format(times, my_num, p_count(times, my_num, is_only=False))

        content['c'] += '--->\n'
        content['c'] += '叫+1\n'
        # 展示当前叫的个数+1，我当前持有的骰数的，不斋概率
        for my_num in my_dices_set:
            content['c'] += '-->{}个{}不斋的概率:{}%\n'.format(times + 1, my_num, p_count(times + 1, my_num, is_only=False))

        content['c'] += '==============================================\n'
        content['c'] += '斋：\n'
        content['c'] += '不+1\n'
        # 展示当前叫的个数，我当前持有的骰数的，斋概率
        for my_num in my_dices_set:
            if my_num > num:
                content['c'] += '-->{}个{}斋的概率:{}%\n'.format(times, my_num, p_count(times, my_num, is_only=True))

        content['c'] += '--->\n'

        # 展示当前叫的个数+1，我当前持有的骰数的，斋概率
        content['c'] += '叫+1\n'
        for my_num in my_dices_set:
            content['c'] += '-->{}个{}斋的概率:{}%\n'.format(times + 1, my_num, p_count(times + 1, my_num, is_only=True))

    get_times_num_probability(int(num[0]), int(num[1]), is_only=int(num[2]))
    content['my_dice'] = my_dice
    content['num'] = num
    print(content['c'])
    return render(request, 'demo.html', content)