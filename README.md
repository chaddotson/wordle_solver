# My Wordle Solver
Here I compare several multiple strategies for solving wordles. 
Success-wise entropy solvers most often get it within 6 attempts. 
Interestingly, using letter positional dominance with the initial 
objective of eliminating letters is fast and very nearly as
successful.

***Note:
Lots of solvers report 100% success rate. I have found those only
use the accepted word list instead of the full word list.***


# Benchmarks
```
                                       Method       Success %   Total Seconds     Avg Seconds       Avg Tries       Max Tries          Failed
                Popular Entropy Elimination 3          99.480         155.182        0.067237           4.308               7              12
            Dominance Entropy Elimination 3/5          99.480          63.561        0.027539           4.346               7              12
            Dominance Entropy Elimination 3/4          99.437          62.498        0.027079           4.349               7              13
           Dominance Entropy Elimination 3/40          99.393          60.521        0.026222           4.345               7              14
           Dominance Entropy Elimination 3/20          99.393          66.763        0.028927           4.345               7              14
          Dominance Entropy Elimination 3/100          99.393          68.052        0.029485           4.345               7              14
            Dominance Entropy Elimination 3/6          99.393          61.914        0.026826           4.346               7              14
           Dominance Entropy Elimination 3/10          99.393          64.483        0.027939           4.347               7              14
            Dominance Entropy Elimination 3/3          99.350          64.425        0.027914           4.360               7              15
           Dominance Entropy Elimination 4/40          99.047          80.073        0.034694           4.566               8              22
                Popular Entropy Elimination 2          98.830         143.574        0.062207           3.910               8              27
                            Popular Entropy 5          98.787         150.613        0.065257           3.914               9              28
                 Rank Entropy Elimination 3 4          98.744          91.803        0.039776           4.495               9              29
                           Popular Entropy 10          98.657         146.824        0.063615           3.907               9              31
                 Rank Entropy Elimination 3 3          98.614          93.608        0.040558           4.506               9              32
                 Rank Entropy Elimination 3 5          98.570          91.930        0.039831           4.491               9              33
                 Rank Entropy Elimination 3 6          98.570          90.154        0.039061           4.492               8              33
                Rank Entropy Elimination 3 10          98.527          90.482        0.039204           4.481               9              34
           Dominance Entropy Elimination 2/40          98.484          65.308        0.028297           4.028               9              35
                Rank Entropy Elimination 3 40          98.440          90.271        0.039112           4.474               9              36
                Rank Entropy Elimination 4 40          98.267          97.915        0.042424           4.631               9              40
                                      Entropy          98.180         149.351        0.064710           3.997               9              42
           Dominance Entropy Elimination 5/40          98.180          87.050        0.037717           4.642               8              42
                           Popular Entropy 40          98.094         150.187        0.065073           3.903               9              44
                Popular Entropy Elimination 4          97.834         183.916        0.079687           5.189               8              50
                Popular Entropy Elimination 5          97.834         215.423        0.093337           5.189               8              50
                Rank Entropy Elimination 2 40          97.617          79.594        0.034486           4.055               9              55
                Rank Entropy Elimination 5 40          97.357         106.524        0.046154           4.727               9              61
                      Dominance Elimination 3          96.274          57.620        0.024965           4.674               9              86
                      Dominance Elimination 4          96.274          78.951        0.034208           4.674               9              86
                      Dominance Elimination 5          96.274          88.208        0.038218           4.674               9              86
                           Rank Elimination 3          95.147          74.941        0.032470           4.765              11             112
                           Rank Elimination 4          95.147         108.175        0.046870           4.765              11             112
                           Rank Elimination 5          95.147         125.369        0.054319           4.765              11             112
                           Rank Elimination 2          92.808          56.759        0.024592           4.576              10             166
                            Dominance (dedup)          92.288          50.888        0.022049           4.642              12             178
                      Dominance Elimination 2          91.854          56.995        0.024695           4.672              11             188
                                 Rank (dedup)          90.685          42.234        0.018299           4.708              11             215
                                         Rank          90.641          44.825        0.019421           4.705              11             216
                                    Dominance          89.905          63.438        0.027486           4.831              12             233

Note:
The word frequency list is incomplete based on the set of wordle words; however, the set is good enough that the
success % is the same as a more complete list.