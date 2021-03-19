from typing import List, Optional


def main():
    with open('exercise-12.txt', 'r') as f:
        lines = f.read().splitlines()

    nums = [int(line) for line in lines]
    idx = search(nums, 50)
    if idx is not None:
        print(idx)
    else:
        print('not found')


def search(nums: List[int], val: int) -> Optional[int]:
    return __search(nums, val, 0, len(nums) - 1)


def __search(nums: List[int], val: int, low: int, high: int) -> Optional[int]:
    mid = int((high + low) / 2)
    mid_val = nums[mid]

    if low == high:
        if mid_val == val:
            return mid
        else:
            return None

    if mid_val > val:
        return __search(nums, val, low, max(mid - 1, 0))
    elif mid_val < val:
        return __search(nums, val, max(mid + 1, 0), high)
    else:
        return mid


if __name__ == '__main__':
    main()
