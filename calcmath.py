import numpy as np

def funcsolve(f, g, lims, e = 1e-4, step = 0.2, min_step = 0.001):
    diff = lambda x: np.power(f(x) - g(x), 2)
    deriv = lambda f, x: np.divide(f(x) - f(x - step), step) #Backward differentiation
    
    def is_converging(x):
        f_val = f(x)
        f_deriv = deriv(f, x)
        
        g_val = g(x)
        g_deriv = deriv(g, x)
        
        #If two lines can converge
        if f_val > g_val:
            return g_deriv > f_deriv
        elif f_val < g_val:
            return f_deriv > g_deriv
        else: #Solution found
            return True
    def could_converge(lim):
        '''
        Does the inequality check
        Needn't worry about equality in either case as would've been checked already
        '''
        start = f(lim[0]) < g(lim[0])
        end = f(lim[1]) < g(lim[1])
        return start ^ end
    
    x = lims[0]
    prevDiff = diff(x)
    
    prev = True #Will increase runtime for faulty ones, but setting initial True will ignore certain cases
    #Prioritizing correctness over efficiency
    while x <= lims[1]:
        '''
        Has converging switched from True to Negative
        '''
        if diff(x) <= e: #Base condition
            return x, True
        
        curr = is_converging(x)
        if prev and not curr: #Was converging and is not now
            pot_lim = [x - step, x]
            if could_converge(pot_lim) and step >= min_step: #Could it have converged; include a lower limit on the step
                return funcsolve(f, g, pot_lim, step = np.divide(step, 10))#Recursive call with smaller range and step
        prev = curr
        x += step
    return 0, False

