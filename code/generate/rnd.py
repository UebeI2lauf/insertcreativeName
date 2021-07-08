import numpy as np
from numpy.core.fromnumeric import std
from scipy.stats.stats import ttest_ind

np.random.seed(42)
# create array of controllgroup
controll_group_f = np.random.randint(0, 100, (1, 50), dtype=np.int32)
controll_group_m = np.random.randint(0, 100, (1, 50), dtype=np.int32)

# create array of errorgroup
controll_error_f = np.random.randint(0, 100, (1, 50), dtype=np.int32)
controll_error_m = np.random.randint(0, 100, (1, 50), dtype=np.int32)

# calc standart deviation and mean
gf = (np.mean(controll_group_f), np.std(controll_group_f))
gm = (np.mean(controll_group_m), np.std(controll_group_m))
ef = (np.mean(controll_error_f), np.std(controll_error_f))
em = (np.mean(controll_error_m), np.std(controll_error_m))

print(f"The mean of the controllgroup (50f): {gf[0]} with an SD: {gf[1]}")
print(f"The mean of the controllgroup (50m): {gm[0]} with an SD: {gm[1]}")
print(f"The mean of the errorgroup (50f): {ef[0]} with an SD: {ef[1]}")
print(f"The mean of the errorgroup (50m): {em[0]} with an SD: {em[1]}")

# calc t-test

# controllgroup vs errorgroup
a = ttest_ind(
    controll_group_f + controll_group_m, controll_error_f + controll_error_m, 1
)
print(
    f"The values for controllgroup (50f/50m) vs errorgroup (50f/50m) are t-value: {a[0]} and p-value: {a[1]}"
)

# controll with in the groups
b = ttest_ind(controll_group_f, controll_group_m, 1)
c = ttest_ind(controll_error_f, controll_error_m, 1)
print(
    f"The values for controllgroup (50f) vs controllgroup (50m) are t-value: {b[0]} and p-value: {b[1]}"
)
print(
    f"The values for errorgroup (50f) vs errorgroup (50m) are t-value: {c[0]} and p-value: {c[1]}"
)


# values between the groups same sex
d = ttest_ind(controll_group_f, controll_error_f, 1)
e = ttest_ind(controll_group_m, controll_error_m, 1)

print(
    f"The values for controllgroup (50f) vs errorgroup (50f) are t-value: {d[0]} and p-value: {d[1]}"
)
print(
    f"The values for controllgroup (50m) vs errorgroup (50m) are t-value: {e[0]} and p-value: {e[1]}"
)

# values between the groups not same sex
f = ttest_ind(controll_group_f, controll_error_m, 1)
g = ttest_ind(controll_group_m, controll_error_f, 1)

print(
    f"The values for controllgroup (50f) vs errorgroup (50m) are t-value: {f[0]} and p-value: {f[1]}"
)
print(
    f"The values for controllgroup (50m) vs errorgroup (50f) are t-value: {g[0]} and p-value: {g[1]}"
)

import seaborn as sns

np.random.seed(111)

all_arr = [
    np.random.uniform(size=20),
    np.random.uniform(size=20),
    np.random.uniform(size=20),
    np.random.uniform(size=20),
    np.random.uniform(size=20),
]

sns.boxplot(data=all_arr)
