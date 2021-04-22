from random import random, randint
import numpy
from PIL import Image, ImageChops, ImageStat, ImageDraw
from square import square


#Input of program is png file with name 'input'
initial_image=Image.open('input.png')
initial_image=initial_image.convert('RGB')


number_of_chromosomes=4
chromosomes=[]
chromosomesImg=[]
fit=[]

#Here u can change size of square.It directly affect on amount of genes that would be in chromosome.
#Value of such squares in chromosome is (512/size_of_square)^2
square_size=4

#this value specify number of loops that program will perform
number_of_generations=200000


#Expand all arrays that involved in processing.Fill chromosomes array with squares with random color from initial image
def initialize_arrays():

    for i in range (number_of_chromosomes):
        chromosomes.append([])
        chromosomesImg.append(None)
        fit.append(None)

    for chromosome in chromosomes:
        for i in range(int(512/square_size)):
            for j in range (int(512/square_size)):
                color=initial_image.getpixel((randint(0,511),randint(0,511)))
                newSquare=square(square_size*j,square_size*i,square_size*j+square_size,square_size*i+square_size,color[0],color[1],color[2])
                chromosome.append(newSquare)

#selecting random pixel in initial image and getting it’s values of color in RGB.
# Then we select random square in image that should mutate and change it’s values on obtained ones.
def mutation():
    global chromosomes
    for chromosome in chromosomes:
        colors = initial_image.getpixel((randint(0,511),randint(0,511)))
        index_of_mutation=randint(0,(int(512/square_size)*int(512/square_size))-1)
        chromosome[index_of_mutation].red=colors[0]
        chromosome[index_of_mutation].green=colors[1]
        chromosome[index_of_mutation].blue=colors[2]


#Taking chromosome array and fill chromosomeImg array with corresponding images
def update_images():
    global chromosomesImg,fit
    for i in range(len(chromosomes)):
        img = Image.new('RGB', (512, 512),color='white')
        for square in chromosomes[i]:
            draw = ImageDraw.Draw(img)
            draw.rectangle([(square.x1,square.y1), (square.x2, square.y2),], fill = (square.red,square.green,square.blue))

        chromosomesImg[i]=numpy.asarray(img)

#compares “mutated images” and initial image and fills array called “fit” with corresponding fit values.
# Then it return indexes of 2 chromosomes that pretend to be parents for next generation
def fitness():
    for i in range(len(chromosomes)):
        fit[i]=sum(ImageStat.Stat(ImageChops.difference(Image.fromarray(chromosomesImg[i]), initial_image)).rms)

    sorted_array=sorted(fit)
    if fit.index(sorted_array[0])!=fit.index(sorted_array[1]):
        return (fit.index(sorted_array[0]),fit.index(sorted_array[1]))
    else:
        arr = numpy.array(fit)
        t=numpy.flatnonzero(arr == arr.min())
        return (t[0],t[1])


#It copy first and second parent to first 2 positions of “chromosomes” array.
# Then its splits each parent on 2 halfes:bottom and top parts.
# First child will be compiled using top part of first parent and bottom part of second, second child will have top part
# of second parent and bottom part of first parent.
# First child will be placed at third index of array,second will occupy fourth cell of an array
def crossover(first_parent_index,second_parent_index):
    first_parent=chromosomes[first_parent_index]
    second_parent=chromosomes[second_parent_index]
    for i in range(len(chromosomes[0])):
        chromosomes[0][i].red=first_parent[i].red
        chromosomes[0][i].blue=first_parent[i].blue
        chromosomes[0][i].green=first_parent[i].green
    for i in range(len(chromosomes[1])):
        chromosomes[1][i].red=second_parent[i].red
        chromosomes[1][i].blue=second_parent[i].blue
        chromosomes[1][i].green=second_parent[i].green

    for i in range(0,int(len(chromosomes[3])/2)):
        chromosomes[2][i].red=first_parent[i].red
        chromosomes[2][i].blue=first_parent[i].blue
        chromosomes[2][i].green=first_parent[i].green
    for i in range(int(len(chromosomes[2])/2),len(chromosomes[3])):
        chromosomes[2][i].red=second_parent[i].red
        chromosomes[2][i].blue=second_parent[i].blue
        chromosomes[2][i].green=second_parent[i].green

    for i in range(0,int(len(chromosomes[3])/2)):
        chromosomes[3][i].red=second_parent[i].red
        chromosomes[3][i].blue=second_parent[i].blue
        chromosomes[3][i].green=second_parent[i].green
    for i in range(int(len(chromosomes[3])/2),len(chromosomes[3])):
        chromosomes[3][i].red=first_parent[i].red
        chromosomes[3][i].blue=first_parent[i].blue
        chromosomes[3][i].green=first_parent[i].green



initialize_arrays()
update_images()
count=0

# Main cycle body.It saves obtained result during operations every 10000 iterations as 'semiresult.png'.
while count<number_of_generations:
    count+=1
    print(count)
    mutation()
    update_images()
    parents=fitness()
    crossover(parents[0],parents[1])
    update_images()
    print(fit[0])
    if count%10000==0:
        semiresult=Image.fromarray(chromosomesImg[0])
        semiresult.save('semiresult.png')



#saving final image as result.png
result=Image.fromarray(chromosomesImg[0])
result.save('result.png')
