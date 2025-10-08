import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.sql.*;

public class AdminPage extends JFrame implements ActionListener {
    JComboBox<String> bloodTypeBox;
    JTextField quantityField, locationField;
    JButton addButton, updateButton;

    public AdminPage() {
        setTitle("🛠 Admin Resource Manager");
        setSize(450, 300);
        setLocationRelativeTo(null);
        setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        setLayout(new GridLayout(4, 2, 10, 10));
        getContentPane().setBackground(new Color(255, 248, 220)); // cornsilk

        add(new JLabel("🩸 Blood Type:"));
        String[] bloodTypes = {"A+", "B+", "O+", "AB+", "O-"};
        bloodTypeBox = new JComboBox<>(bloodTypes);
        add(bloodTypeBox);

        add(new JLabel("📦 Quantity Units:"));
        quantityField = new JTextField();
        add(quantityField);

        add(new JLabel("📍 Location:"));
        locationField = new JTextField();
        add(locationField);

        addButton = new JButton("➕ Add Resource");
        addButton.setBackground(new Color(60, 179, 113));
        addButton.setForeground(Color.WHITE);
        addButton.addActionListener(this);
        add(addButton);

        updateButton = new JButton("🔄 Update Quantity");
        updateButton.setBackground(new Color(70, 130, 180));
        updateButton.setForeground(Color.WHITE);
        updateButton.addActionListener(this);
        add(updateButton);

        setVisible(true);
    }

    public void actionPerformed(ActionEvent e) {
        String bloodType = (String) bloodTypeBox.getSelectedItem();
        String quantityText = quantityField.getText().trim();
        String location = locationField.getText().trim();

        if (quantityText.isEmpty() || location.isEmpty()) {
            JOptionPane.showMessageDialog(this, "❌ Please fill in all fields.");
            return;
        }

        try {
            int quantity = Integer.parseInt(quantityText);
            Connection conn = DriverManager.getConnection(
                    "jdbc:mysql://localhost:3306/dronedb", "root", "Sathishdhana#23"
            );

            if (e.getSource() == addButton) {
                String insertQuery = "INSERT INTO blood_inventory (blood_type, quantity_units, location) VALUES (?, ?, ?)";
                PreparedStatement stmt = conn.prepareStatement(insertQuery);
                stmt.setString(1, bloodType);
                stmt.setInt(2, quantity);
                stmt.setString(3, location);
                stmt.executeUpdate();
                JOptionPane.showMessageDialog(this, "✅ Resource added successfully!");
            } else if (e.getSource() == updateButton) {
                String updateQuery = "UPDATE blood_inventory SET quantity_units = quantity_units + ? WHERE blood_type = ?";
                PreparedStatement stmt = conn.prepareStatement(updateQuery);
                stmt.setInt(1, quantity);
                stmt.setString(2, bloodType);
                stmt.executeUpdate();
                JOptionPane.showMessageDialog(this, "✅ Quantity updated successfully!");
            }

            conn.close();
        } catch (NumberFormatException ex) {
            JOptionPane.showMessageDialog(this, "❌ Quantity must be a number.");
        } catch (SQLException ex) {
            JOptionPane.showMessageDialog(this, "❌ Database error: " + ex.getMessage());
        }
    }
}