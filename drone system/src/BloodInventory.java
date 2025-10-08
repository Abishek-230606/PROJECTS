import java.util.ArrayList;
import java.util.List;

public class BloodInventory {

    public static List<String> getAllItems() {
        List<String> items = new ArrayList<>();

        // Sample inventory data — you can replace this with JDBC logic later
        items.add("A+ : 10 units");
        items.add("B+ : 8 units");
        items.add("O- : 5 units");
        items.add("AB+ : 3 units");
        items.add("A- : 6 units");
        items.add("B- : 4 units");

        return items;
    }
}
