# wordle_solver
My wordle solver. Interesting comparison of multiple strategies. 
Success-wise entropy solvers most often get it within 6 attempts. 
Interestingly, using letter positional dominance with the initial 
objective of eliminating letters is fast and very nearly as
successful.


# Benchmarks
```
                             Method       Success %   Total Seconds     Avg Seconds       Avg Tries       Max Tries
    Dominance Entropy Elimination 3          99.307         150.367        0.065150           4.349               7
         Rank Entropy Elimination 3          99.307         135.490        0.058705           4.349               7
    Dominance Entropy Elimination 4          99.047         175.367        0.075982           4.568               8
         Rank Entropy Elimination 4          99.047         150.105        0.065037           4.568               8
      Popular Entropy Elimination 4          98.873         287.739        0.124670           4.336               8
      Popular Entropy Elimination 5          98.873         289.745        0.125539           4.336               8
      Popular Entropy Elimination 3          98.873         335.967        0.145566           4.336               8
      Popular Entropy Elimination 2          98.787         323.918        0.140346           3.909               9
    Dominance Entropy Elimination 2          98.354         157.135        0.068083           4.028               9
         Rank Entropy Elimination 2          98.354         151.075        0.065457           4.028               9
                    Popular Entropy          98.267         319.640        0.138492           3.900               9
    Dominance Entropy Elimination 5          98.224         183.384        0.079456           4.642               8
         Rank Entropy Elimination 5          98.224         141.402        0.061266           4.642               8
                            Entropy          98.180         322.409        0.139692           3.997               9
            Dominance Elimination 3          96.274         140.130        0.060715           4.674               9
            Dominance Elimination 4          96.274         190.101        0.082366           4.674               9
            Dominance Elimination 5          96.274         210.529        0.091217           4.674               9
                 Rank Elimination 5          95.104         290.896        0.126038           4.766              11
                 Rank Elimination 3          95.104         187.894        0.081410           4.766              11
                 Rank Elimination 4          95.104         255.886        0.110869           4.766              11
                 Rank Elimination 2          92.851         145.335        0.062970           4.576              10
                  Dominance (dedup)          92.288         120.527        0.052221           4.642              12
            Dominance Elimination 2          91.854         136.074        0.058958           4.672              11
                       Rank (dedup)          90.685         115.205        0.049916           4.708              11
                               Rank          90.641         116.372        0.050421           4.705              11
                          Dominance          89.905         150.893        0.065378           4.831              12
```

Note:
The word frequency list is incomplete based on the set of wordle words; however, the set is good enough that the
success % is the same as a more complete list.