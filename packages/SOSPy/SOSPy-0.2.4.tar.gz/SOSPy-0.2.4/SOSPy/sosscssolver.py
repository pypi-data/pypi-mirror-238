import numpy as np
import scs
from scipy.sparse import csc_matrix
from scipy.linalg import block_diag
import time

# The vec function as documented in api/cones
def vec(S):
    n = S.shape[0]
    S = np.copy(S)
    S *= np.sqrt(2)
    S[range(n), range(n)] /= np.sqrt(2)
    return S[np.triu_indices(n)]

# The mat function as documented in api/cones
def mat(s):
    n = int((np.sqrt(8 * len(s) + 1) - 1) / 2)
    S = np.zeros((n, n))
    S[np.triu_indices(n)] = s / np.sqrt(2)
    S = S + S.T
    S[range(n), range(n)] /= np.sqrt(2)
    return S

def restore_symmetric_matrix(upper_triangle_values,n):    
    matrix = [0]*(n**2)
    
    idx = 0
    for i in range(n):
        for j in range(i, n):
            matrix[i*n+j] = upper_triangle_values[idx]
            matrix[j*n+i] = upper_triangle_values[idx] 
            idx += 1
    
    return matrix

def sosscssolver(At,b,c,K,options={},verbose=1):
    if 'q' in K:
        raise Exception('K.q and K.r are supposed to be empty')

    if 'f' not in K:
        K['f'] = []
    if 'l' not in K:
        K['l'] = []

    nf = int(np.sum(K['f']))
    nl = int(np.sum(K['l']))

    Ks2 = [int(item**2) for item in K['s']]
    Kindex = nf + nl + np.cumsum([0]+Ks2)
    RSPind = Ks2 + [nf]

    nsdpvar = len(K['s'])   # Number of Semidefinite Program Variables
    nvars = Kindex[0]       # Number of scalar variable


    ############################### process b ##################################
    ncons = At.shape[1]  # number of constraints
    b_z = b.toarray().flatten()

    ############################# process A and c #############################
    A = []
    C = []
    A_psd = []
    totalpsd = 0
    LEN_VAR = [nvars]
    #### sdp variable
    for i in range(nsdpvar):
        C.append(vec(c[Kindex[i]:Kindex[i+1]].reshape(K['s'][i],K['s'][i]).toarray()))
        npsdvars = int(K['s'][i]*(K['s'][i]+1)/2)
        totalpsd = totalpsd + npsdvars
        LEN_VAR.append(totalpsd+nvars)
        A_psd.append(-1*np.eye(npsdvars))  # for psd cones
        #A_psd.append(np.diag(-1*np.ones((npsdvars,))/vec(np.ones((K['s'][i],1)) @ np.ones((K['s'][i],1)).T)))  # for psd cones
        #A_psd.append(np.diag(-1*vec(np.ones((K['s'][i],1)) @ np.ones((K['s'][i],1)).T)))  # for psd cones
        A_temp = []
        for j in range(ncons):
            A_temp.append(vec(At[Kindex[i]:Kindex[i+1],j].toarray().flatten().reshape((K['s'][i],K['s'][i]))))
        A.append(np.vstack(A_temp))
        
    A_z = np.hstack(A)
    c_scs = np.hstack(C)
    A_p = np.hstack((np.zeros((totalpsd,nvars)),block_diag(*A_psd)))
    b_p = np.zeros(totalpsd)

    #### scalar variable
    if nvars>0:
        c_scs = np.hstack((c[:nvars].toarray().flatten(), c_scs))
        A_z = np.hstack((At[:nvars,:].toarray().T, A_z))
        
    ############################### Collect A,b,c,P ###############################
    A_scs = csc_matrix(np.vstack((A_z,A_p)))
    P_scs = csc_matrix(np.zeros((A_scs.shape[1],A_scs.shape[1])))
    b_scs = np.hstack((b_z,b_p))

    ################################ collect dim ##################################
    if nsdpvar > 1:
        s_dim = K['s']
    else:
        s_dim = K['s'][0]

    ################################# options ####################################
    if 'max_iters' in options:
        max_iters = options['max_iters']
    else:
        max_iters = 100000

    if verbose == 1:
        verbose = True
    else:
        verbose = False
    
    ################################# solve #######################################
    z_dim = b_z.shape[0]
    data = dict(P=P_scs, A=A_scs, b=b_scs, c=c_scs)
    cone = dict(z=z_dim,s=s_dim)
    # Initialize solver
    solver = scs.SCS(data, cone, eps_abs=1e-9, eps_rel=1e-9, max_iters=max_iters, verbose=verbose)
    # Solve
    start_time = time.time()
    sol = solver.solve()
    end_time = time.time()


    ################################# post process ################################
    sol_conv = []   # solution converted to standard form
    sol_conv.extend([1]*nvars) # number of scalar variables
    for i in range(nsdpvar):
        K_size = np.ones((K['s'][i],1))
        sol_conv.extend(vec(K_size @ K_size.T).tolist())

    sol_inv = np.linalg.inv(np.diag(sol_conv))
    
    x_temp = [item for item in sol_inv @ sol['x']]
    x = []
    x.extend(x_temp[:nvars])
    for i in range(nsdpvar):
        x.extend(restore_symmetric_matrix(x_temp[LEN_VAR[i]:LEN_VAR[i+1]],K['s'][i]))

    y = [item for item in sol['y'][:ncons]]

    info = {}
    info['cpusec'] = round(end_time-start_time,5)
    info['iter'] = sol['info']['iter']
    info['status'] = sol['info']['status']
    info['pinf'] = round(sol['info']['res_pri'],5)
    info['dinf'] = round(sol['info']['res_dual'],5)
 
    return x, y, info

