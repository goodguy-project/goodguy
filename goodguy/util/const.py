import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

PLATFORM_ALL = ['codeforces', 'nowcoder', 'atcoder', 'leetcode']

if __name__ == '__main__':
    print(locals())
