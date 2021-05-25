package dk.itu.mario.engine.level;

import java.util.Random;
import java.util.*;

//Make any new member variables and functions you deem necessary.
//Make new constructors if necessary
//You must implement mutate() and crossover()


public class MyDNA extends DNA
{
	
	public int numGenes = 0; //number of genes
	private Random rand = new Random(1);

	// Return a new DNA that differs from this one in a small way.
	// Do not change this DNA by side effect; copy it, change the copy, and return the copy.
	public MyDNA mutate ()
	{
		MyDNA copy = new MyDNA();
		//YOUR CODE GOES BELOW HERE
		copy.setChromosome(this.getChromosome());

		int index = rand.nextInt((30 / 2) * 2);
//		System.out.println(index);
		//String replaced = "";
		for (int i = index; i < index + 7; i += 2) {
			//System.out.println(i);
			if (i > 28) {
				break;
			}

			char block = 'A';
			int block_code = rand.nextInt(5);
			int len = rand.nextInt(6) + 1;
			switch(block_code) {
			case 0:
				block = 'G'; // gap
				break;
			case 1:
				block = 'S'; // stair
				break;
			case 2:
				block = 'C'; // coin
				break;
			case 3:
				block = 'E'; // enemy
				break;
			default:
				block = 'F'; // floor
			}

			String chunk = Character.toString(block) + Integer.toString(len);
//			System.out.println(chunk);
//			System.out.println(copy.getChromosome().length());
			String newChrom = copy.getChromosome().substring(0, i + 1) + chunk + copy.getChromosome().substring(i + 3);
			String secondPart = copy.getChromosome().substring(i + 1);
			copy.setChromosome(newChrom);

		}

//		String newChrom = copy.getChromosome().substring(0, index) + replaced + copy.getChromosome().substring(index + 7);
//		copy.setChromosome(newChrom);

		//YOUR CODE GOES ABOVE HERE
		return copy;
	}
	
	// Do not change this DNA by side effect
	public ArrayList<MyDNA> crossover (MyDNA mate)
	{
		ArrayList<MyDNA> offspring = new ArrayList<MyDNA>();
		//YOUR CODE GOES BELOW HERE

		String crom1 = this.getChromosome();
		String crom2 = mate.getChromosome();
//		System.out.println(crom1.length());
//		System.out.println(crom2.length());
		int split = rand.nextInt(crom1.length());

		String off1 = crom1.substring(0, split) + crom2.substring(split);
		String off2 = crom2.substring(0, split) + crom1.substring(split);

		MyDNA child1 = new MyDNA();
		MyDNA child2 = new MyDNA();

		child1.setChromosome(off1);
		child2.setChromosome(off2);

		offspring.add(child1);
		offspring.add(child2);

		//YOUR CODE GOES ABOVE HERE
		return offspring;
	}
	
	// Optional, modify this function if you use a means of calculating fitness other than using the fitness member variable.
	// Return 0 if this object has the same fitness as other.
	// Return -1 if this object has lower fitness than other.
	// Return +1 if this objet has greater fitness than other.
	public int compareTo(MyDNA other)
	{
		int result = super.compareTo(other);
		//YOUR CODE GOES BELOW HERE
		
		//YOUR CODE GOES ABOVE HERE
		return result;
	}
	
	
	// For debugging purposes (optional)
	public String toString ()
	{
		String s = super.toString();
		//YOUR CODE GOES BELOW HERE
		
		//YOUR CODE GOES ABOVE HERE
		return s;
	}
	
	public void setNumGenes (int n)
	{
		this.numGenes = n;
	}

}

