import numpy as np
from matrix import M as M_old, names as old_names
FINAL=["Website development","Data Science","Data Analysis","Embedded Systems","IoT","Machine Learning","3D design","Project management","Research and development","Product design","Network Engineering","Cybersecurity","Graphic design","Robotics","UI/UX","Digital Marketing","Cooking","Python","Creative Writing","Electrical Installation"]
norm=lambda s:s.lower().replace('&','and')
perm=[[norm(x) for x in old_names].index(norm(s)) for s in FINAL]
M=M_old[np.ix_(perm,perm)]
assert np.allclose(M,M.T) and np.allclose(np.diag(M),0)
DOMAIN={"Website development":"SW","Data Science":"SW","Data Analysis":"SW","Machine Learning":"SW","Python":"SW",
"Embedded Systems":"HW","IoT":"HW","Robotics":"HW","Electrical Installation":"HW",
"3D design":"DES","Product design":"DES","Graphic design":"DES","UI/UX":"DES",
"Project management":"BIZ","Digital Marketing":"BIZ","Creative Writing":"BIZ",
"Network Engineering":"NET","Cybersecurity":"NET","Research and development":"MISC","Cooking":"MISC"}
if __name__=='__main__':
    import csv
    with open('/home/claude/sim/M_final_order.csv','w',newline='') as f:
        w=csv.writer(f); w.writerow(['skill']+[f'S{i}' for i in range(20)])
        for i,s in enumerate(FINAL): w.writerow([f'S{i} {s}']+[M[i,j] for j in range(20)])
    print('final-order matrix saved; symmetric, zero diagonal; range',M[M>0].min(),M.max())
    for i in (0,17,14): print(i,FINAL[i],M[i,:5])
