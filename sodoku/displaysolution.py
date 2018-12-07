def p(i,j,d):
  return str((((i-1)*9)+(j-1))*9 + d)

def main():

  line = input()

  if line.strip() == "SAT":
    print("Solution is:")

    solution = set(input().split())

    for i in range(1,10):
      for j in range(1,10):
        for d in range(1,10):
          if str(p(i,j,d)) in solution:
            print(str(d)+' ', end="")
      print()

  else:
    print("NO SOLUTION")


main()
