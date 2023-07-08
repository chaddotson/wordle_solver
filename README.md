# wordle_solver
My wordle solver. Interesting comparison of multiple strategies. 
Success-wise entropy solvers most often get it within 6 attempts. 
Interestingly, using letter positional dominance with the initial 
objective of eliminating letters is fast and very nearly as
successful.


# Benchmarks
```
                        Method       Success %   Total Seconds     Avg Seconds       Avg Tries       Max Tries
               Popular Entropy          98.267         167.209        0.072448           3.900               9
                       Entropy          98.180         168.566        0.073035           3.997               9
         Dominance Elimination          96.274          86.296        0.037390           4.674               9
             Dominance (dedup)          92.288          77.227        0.033461           4.642              12
                  Rank (dedup)          90.685          71.269        0.030879           4.708              12
                          Rank          90.641          73.539        0.031863           4.706              12
                     Dominance          89.905          91.129        0.039484           4.831              12
```

Note:
The word frequency list is incomplete based on the set of wordle words; however, the set is good enough that the
success % is the same as a more complete list.