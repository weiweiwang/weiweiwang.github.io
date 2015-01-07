title: 随机抽样问题
slug: reservoir-sampling
category: programming
tags: random sampling,reservoir sampling
date: 2012-10-19

#问题
    
        要求从N个元素中随机的抽取k个元素，其中N无法确定。

# 伪代码


        Init : a reservoir with the size： k
             for i= k+1 to N
                  M=random(1, i);
                  if( M <= k)
                     SWAP the Mth value and ith value
             end for

#证明
初始情况: i<=k,i个元素全部放入水库，每个元素出现在水池的概率为1。

假设k<=j<=i时结论成立。

当j=i+1,第i+1个元素会以k/(i+1)的概率被选中, 前i个元素在本次替换操作完成时出现在水池的概率分解为：

        1) 在i+1选择前出现在水池中,这个概率是k/i
        2) 并且在i+1次没有被替换掉,这个概率=1-这个元素被替换掉的概率=1-k/(i+1)*(1/k)=i/(i+1)

所以前i个元素出现在水池的概率为(k/i)*(i/(i+1))=k/(i+1)

由归纳法可知结论成立。

