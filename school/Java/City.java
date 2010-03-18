public class City {
    private String name;
    private int population;
    
    public City(){
	population = 0;
    }
    
    public City(String name){
	population = 0;
	this.name = name;
    }
    
    public City(String name, int population){
	this.population = population;
	this.name = name;
    }
    
    public void setName(String name){
	this.name = name;
    }
    
    public void setPopulation(int population){
	this.population = population;
    }
    
    public String getName() { return name; }
    public int getPopulation() { return population; }
    
    public static void main(String[] args){
	City a = new City()
	a.setPopulation(3000000)
	a.setName("Ankara")
	
	City c = new City("Istanbul");
	c.setPopulation(12000000);
	System.out.println(c.getName() + " with "+ c.getPopulation() + " population");
	
	City i = new City("Izmir", 2000000);
	System.out.println(i.getName() + " with "+ i.getPopulation() + " population");
    }
    
}