def sp(value: int, units: str = None, name: str = None):
  '''
  Convert a number to scientific notation
  '''
  sv = f'{value:.3e}'.split('e')
  ss = sv[0] + '*10^' + sv[1]
  if units is None and name is not None:
    print(name, '=', ss)
  elif name is None and units is not None:
    print(ss, units)
  elif name is None and units is None:
    print(ss)
  else:
    print(name, '=', ss, units)

def lrp(x: list, y: list, title: str = None):
  '''
  Make a linear regression and plot the result
  '''
  import matplotlib.pyplot as plt
  from sklearn.linear_model import LinearRegression
  import pandas as pd
  df = pd.DataFrame(data={'x': x, 'y': y})
  x = df[['x']]
  y = df[['y']]
  clf = LinearRegression()
  clf.fit(x, y)
  r = clf.predict(x)
  m = clf.coef_
  b = clf.intercept_
  fig, ax = plt.subplots(layout='constrained')
  ax.plot(x, y, label='Original')
  ax.scatter(x,y)
  ax.set_title(f"y = {m[0][0]:.3} * x + {b[0]:.3}", loc='right',fontsize=10)
  if title is None:
    fig.suptitle('Linear Regression')
  else:
    fig.suptitle(f'{title}')
  ax.plot(x, r, linestyle='--', label='Regression')
  ax.grid()
  ax.legend()
  plt.show()