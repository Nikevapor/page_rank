from bs4 import BeautifulSoup
from math import ceil
import urllib2
import re

#defined site and limit
site = 'http://www.kpfu.ru/'
pages_count = 100

#defined list of web pages
html_page = urllib2.urlopen(site)
soup = BeautifulSoup(html_page, 'lxml')
i = 0
list = []
for link in soup.findAll('a', href=re.compile("^http://kpfu.ru/")):
    if (link.get('href') not in list):
        i += 1
        if (i == 1):
            with open('pages.txt', 'w') as f:
                f.write(str(i) + ". " + str(link.get('href')) + "\n")
        else :
            with open('pages.txt', 'a') as f:
                f.write(str(i) + ". " + str(link.get('href')) + "\n")
        list.append(str(link.get('href')))
    if (i == pages_count):
        break

#defined and init variables
matrix = [[0 for x in range(len(list))] for y in range(len(list))]
page_links = []
i = 0
k = 0

#task1
#creating adjacency matrix
for i in range(len(list)):
    html_page = urllib2.urlopen(list[i])
    soup = BeautifulSoup(html_page, 'lxml')
    links = soup.findAll('a', href=re.compile("^http://kpfu.ru/"))
    for link in links:
        page_links.append(str(link.get('href')))
    for k in range(len(list)):
        if ((list[k] in page_links) and (i != k)):
            matrix[i][k] = 1
        else:
            matrix[i][k] = 0
    page_links = []
#output adjacency matrix
with open('adj_matrix.txt', 'w') as f:
    for _list in matrix:
        for _number in _list:
            f.write(str(_number) + " ")
        f.write('\n')

#task2
#defined lists for task2
matrix_ranks = [0 for x in range(len(matrix))]
matrix_count_links = [0 for x in range(len(matrix))]

count = 0

#counts how many links current web page has using adj. matrix
for i in range(len(list)):
    for k in range(len(list)):
        if (matrix[i][k] == 1):
            count += 1
    matrix_count_links[i] = count
    count = 0

#only 2 iterations...
for i in range(len(matrix)):
    for k in range (len(matrix)):
        if ((i != k) and (matrix[k][i] == 1) ):
            top_rank = 1.0 / matrix_count_links[k]
            for j in range(len(matrix)):
                if ((j != k) and (matrix[j][k] == 1)):
                    matrix_ranks[i] += 1.0 / matrix_count_links[j] * 1.0 / len(matrix) * top_rank

with open('matrix_ranks.txt', 'w') as f:
    for _list in matrix_ranks:
        f.write(str(_list))
        f.write('\n')

result_matrix = []

#sorting
def getKey(item):
    return item[1]

for i in range(len(list)):
    result_matrix.append([list[i], matrix_ranks[i]])
result_matrix.sort(reverse=True, key=getKey)
with open('result_rank.txt', 'w') as f:
    for _list in result_matrix:
        f.write(str(_list))
        f.write('\n')

#example from lecture presentation

# matrix = [
#     [0, 1, 0, 0, 0],
#     [0, 0, 0, 0, 1],
#     [1, 1, 0, 1, 1],
#     [0, 0, 1, 0 ,1],
#     [0, 0, 0, 1, 0]
# ]
# matrix_ranks = [0 for x in range(len(matrix))]
# matrix_count_links = [0 for x in range(len(matrix))]
#
#
# for i in range(len(matrix)):
#     for k in range(len(matrix)):
#         if (matrix[i][k] == 1):
#             count += 1
#     matrix_count_links[i] = count
#     #matrix_ranks[i] = matrix_ranks[i] + 1.0 / len(list) * 1.0 / count
#     count = 0
#
#
# for i in range(len(matrix)):
#     for k in range (len(matrix)):
#         if ((i != k) and (matrix[k][i] == 1) ):
#             top_rank = 1.0 / matrix_count_links[k]
#             for j in range(len(matrix)):
#                 if ((j != k) and (matrix[j][k] == 1)):
#                     matrix_ranks[i] += 1.0 / matrix_count_links[j] * 1.0 / len(matrix) * top_rank
# print [row[1] for row in matrix]
# with open('matrix_ranks.txt', 'w') as f:
#     for _list in matrix_ranks:
#         f.write(str(_list))
#         f.write('\n')
