import javax.swing.*;
import java.awt.*;
import java.util.List;

public class DashboardPage extends JFrame {
    private String username;

    public DashboardPage(String username) {
        this.username = username;
        setTitle("Dashboard");
        setSize(500, 400);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLocationRelativeTo(null);

        JLabel welcomeLabel = new JLabel("Welcome, " + username);
        welcomeLabel.setHorizontalAlignment(SwingConstants.CENTER);
        welcomeLabel.setFont(new Font("Arial", Font.BOLD, 16));

        // Inventory display
        JTextArea inventoryArea = new JTextArea();
        inventoryArea.setEditable(false);
        inventoryArea.setFont(new Font("Monospaced", Font.PLAIN, 14));

        List<String> items = BloodInventory.getAllItems(); // ✅ Correct reference
        if (items != null && !items.isEmpty()) {
            for (String item : items) {
                inventoryArea.append(item + "\n");
            }
        } else {
            inventoryArea.setText("No inventory items found.");
        }

        JScrollPane scrollPane = new JScrollPane(inventoryArea);

        JButton orderButton = new JButton("Go to Order Page");
        orderButton.addActionListener(e -> {
            new OrderPage(username); // Make sure OrderPage accepts username
            dispose();
        });

        JPanel panel = new JPanel(new BorderLayout());
        panel.add(welcomeLabel, BorderLayout.NORTH);
        panel.add(scrollPane, BorderLayout.CENTER);
        panel.add(orderButton, BorderLayout.SOUTH);

        add(panel);
        setVisible(true);
    }
}