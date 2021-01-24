####################################################################
# Homework 4                                                       #
#                                                                  #
# Program to calculate the wealth at retirement                    #
#                                                                  #
# Creates a GUI that calculates wealth for 70 years 10 times,      #
# takes it's average and displays the result in the GUI            #
#                                                                  #
# @author Gautam Sharma                                            #
####################################################################

from tkinter import *               # import everything from tkinter
import numpy as np                  # import numpy for arrays
import matplotlib                   # for plots
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

NUMBER_OF_YEARS = 70                # number of years to run a single simulation for

# define the field names and their indices
FIELD_NAMES = ['Mean Return (%)', 'Std Dev Return (%)', 'Yearly Contribution ($)',
               'No. of Years of Contribution', 'No. of Years to Retirement', 'Annual Spend in Retirement']

M_RATE = 0                                         # index for annual mean return rate
SIGMA = 1                                          # index for standard deviation
CONTRIBUTION = 2                                   # index for yearly contribution
CONTRIBUTION_YEARS = 3                             # index for number of years of contribution
RETIREMENT_YEARS  = 4                              # index for number of years to retirement
RETIREMENT_SPEND = 5                               # index for annual spend in retirement
NUM_FIELDS = 6                                     # how many fields there are
NUM_SIM = 10                                       # number of simulations
x_axis = [x for x in range(NUMBER_OF_YEARS+1)]     # number of years for plot


########################################################################################
# Function to make sure that wealth at any year is above 0. If not make a note of it   #
# Input:                                                                               #
#    i - current year                                                                  #
#    wealth - list of wealth accumulated till current year                             #
#    is_neg - keeps track if wealth goes beyond 0                                      #
# Output:                                                                              #
#    if wealth < 0 then returns year at which it is < 0 ,True                          #
#    else return None, False                                                           #
########################################################################################
def check_wealth(i, wealth, is_neg):
    if wealth[i + 1] < 0 and not is_neg:            # check to see if wealth is less than zero at any year
        return i+1, True                            # if wealth < 0 then return current year and True
    return None, False                              # if wealth > 0 then all good


################################################################################
# Function to compute monthly payment to get to final amount in specified time #
# Input:                                                                       #
#    entries - the list of entry fields                                        #
# Output:                                                                      #
#    only output is to screen (for debug) and the GUI                          #
################################################################################
def monthly_payment(entries):

    wealth_avg = []                                              # list that stores the total wealth at end of 70th year
    r = (float(entries[M_RATE].get()) / 100)                     # dividing by 100 to make formula easier
    sigma = float(entries[SIGMA].get())                          # get standard deviation from the user
    contribution = float(entries[CONTRIBUTION].get())            # get yearly contribution from the user
    contribution_years = int(entries[CONTRIBUTION_YEARS].get())  # get years of contribution from the user
    retirement_years = int(entries[RETIREMENT_YEARS].get())      # number of years to retirement
    retirement_spend = float(entries[RETIREMENT_SPEND].get())    # amount spent per year during retirement

    for sim in range(NUM_SIM):               # total number of simulations to run

        # generate 1d array of random number to incorporate market fluctuations
        noise = (sigma / 100) * np.random.randn(70)

        wealth = np.zeros(71, dtype=float)   # wealth array initialised to 0. represents wealth at each year
        wealth[0] = 0                        # wealth at 0th year = 0
        neg_wealth_index = 0                 # to mark the index where the wealth goes negative
        is_neg = False                       # boolean variable to keep track when the wealth goes negative

        # for contributing years add up the yearly contribution
        for i in range(contribution_years):
            wealth[i + 1] = wealth[i] * (1 + r + noise[i]) + contribution
            neg_wealth_index, is_neg = check_wealth(i, wealth, is_neg)  # is wealth less than zero at any year?

        # if not contributing till the start of retirement
        for i in range(contribution_years, retirement_years):
            wealth[i + 1] = wealth[i] * (1 + r + noise[i])
            neg_wealth_index, is_neg = check_wealth(i, wealth, is_neg)  # is wealth less than zero at any year?

        # during retirement just hope that you can sustain with your retirement spending
        for i in range(retirement_years, NUMBER_OF_YEARS):
            wealth[i + 1] = wealth[i] * (1 + r + noise[i]) - retirement_spend
            neg_wealth_index, is_neg = check_wealth(i, wealth, is_neg)  # is wealth less than zero at any year?

        if not is_neg:                                                  # if wealth not below 0 then plot normally
            plt.plot(x_axis, wealth, '+-')
        else:                                                           # else plot the positive values
            plt.plot(x_axis[0:neg_wealth_index], wealth[0:neg_wealth_index], '+-')

        wealth_avg.append(wealth[NUMBER_OF_YEARS])       # add the wealth accumulated at the last year to the list

    plt.ylim(bottom=-0.5)                                # y axis starts at -0.5 to verify that wealth remains > 0
    wealth_avg = sum(wealth_avg) / len(wealth_avg)       # average wealth at end of ten simulations
    wealth_disp = ("%8.2f" % wealth_avg).strip()         # making wealth ready to be displayed
    wealth_var.set(wealth_disp)                          # set the label to the average wealth calculated
    plt.xlabel('years')
    plt.ylabel('wealth')
    plt.title('Wealth Over 70 Years')
    plt.show()                                           # plot the 10 simulations


################################################################################
# Function to create the GUI                                                   #
# Inputs:                                                                      #
#    root - the handle for the GUI                                             #
# Outputs:                                                                     #
#    entries - the list of entry fields                                        #
################################################################################

def makeform(root):
    entries = []                                        # create an empty list
    for index in range(NUM_FIELDS):                     # for each of the fields to create
        row = Frame(root)                               # get the row and create the label
        lab = Label(row, width=22, text=FIELD_NAMES[index]+": ", anchor='w')
        ent = Entry(row)                                # create the entry and init to 0
        ent.insert(0, "0")

        # fill allows the widget to take extra space: X, Y, BOTH, default=NONE
        # expand allows the widget to use up sapce in the parent widget
        row.pack(side=TOP, fill=X, padx=5, pady=5)      # place it in the GUI
        lab.pack(side=LEFT)
        ent.pack(side=RIGHT, expand=YES, fill=X)
        entries.append(ent)                             # add it to the list

    return entries                                      # and return the list


#######################################################################################################################
# Start of the main program...                                                                                        #
#######################################################################################################################

root = Tk()                                                                        # instantiating tkinter constructor
root.title("Wealth Retirement Calculator")                                         # set title
ents = makeform(root)                                                              # get lists of entries

# instantiating a double variable to store the wealth value to be displayed
wealth_var = DoubleVar()
wealth_var.set('')                                                                 # setting it to empty
row = Frame(root)                                                                  # grab a frame from the root
wealth_label = Label(row, width=22,text='Wealth at Retirement ($): ', anchor='w')  # create a wealth at retirement label
row.pack(side=TOP, fill=X, padx=5, pady=5)
wealth_label.pack(side=LEFT)

# create a label to display the wealth at retirement value
wealth_label_val = Label(row, textvariable = wealth_var , anchor='w')
wealth_label_val.pack(side=RIGHT, fill=X, expand=YES)

# add calculate button
b1 = Button(root,width=12,text='Calculate', highlightbackground='#008000',command=(lambda e=ents: monthly_payment(e)))
b1.pack(side=LEFT,  padx=5, pady=5)

# add quit button
b2 = Button(root,width=12,text='Quit',highlightbackground='#ff0000',command=root.destroy)
b2.pack(side=LEFT, padx=5, pady=5)

root.mainloop()                                                                             # start execution

#######################################################################################################################
# End of the program                                                                                                  #
#######################################################################################################################
