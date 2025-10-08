import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.sql.*;

public class OrderPage extends JFrame implements ActionListener {
    JTextField nameField, unitsField, addressField;
    JComboBox<String> bloodTypeBox;
    JButton submitButton;
    String userPassword;

    public OrderPage(String userPassword) {
        this.userPassword = userPassword;

        setTitle("🛒 Place Blood Order");
        setSize(450, 350);
        setLocationRelativeTo(null);
        setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        setLayout(new BorderLayout());

        JLabel header = new JLabel("Place Your Blood Order", SwingConstants.CENTER);
        header.setFont(new Font("Verdana", Font.BOLD, 20));
        header.setForeground(Color.WHITE);
        header.setOpaque(true);
        header.setBackground(new Color(178, 34, 34));
        add(header, BorderLayout.NORTH);

        JPanel formPanel = new JPanel(new GridBagLayout());
        formPanel.setBackground(new Color(245, 245, 255));
        GridBagConstraints gbc = new GridBagConstraints();
        gbc.insets = new Insets(10, 10, 10, 10);
        gbc.fill = GridBagConstraints.HORIZONTAL;

        gbc.gridx = 0; gbc.gridy = 0;
        formPanel.add(new JLabel("👤 Patient Name:"), gbc);
        gbc.gridx = 1;
        nameField = new JTextField();
        formPanel.add(nameField, gbc);

        gbc.gridx = 0; gbc.gridy = 1;
        formPanel.add(new JLabel("🩸 Blood Type:"), gbc);
        gbc.gridx = 1;
        String[] bloodTypes = {"A+", "B+", "O+", "AB+", "O-"};
        bloodTypeBox = new JComboBox<>(bloodTypes);
        formPanel.add(bloodTypeBox, gbc);

        gbc.gridx = 0; gbc.gridy = 2;
        formPanel.add(new JLabel("📦 Units Required:"), gbc);
        gbc.gridx = 1;
        unitsField = new JTextField();
        formPanel.add(unitsField, gbc);

        gbc.gridx = 0; gbc.gridy = 3;
        formPanel.add(new JLabel("📍 Delivery Address:"), gbc);
        gbc.gridx = 1;
        addressField = new JTextField();
        formPanel.add(addressField, gbc);

        gbc.gridx = 0; gbc.gridy = 4; gbc.gridwidth = 2;
        submitButton = new JButton("✅ Submit Order");
        submitButton.setBackground(new Color(0, 128, 128));
        submitButton.setForeground(Color.WHITE);
        submitButton.setFont(new Font("Arial", Font.BOLD, 14));
        submitButton.addActionListener(this);
        formPanel.add(submitButton, gbc);

        add(formPanel, BorderLayout.CENTER);
        setVisible(true);
    }

    public void actionPerformed(ActionEvent e) {
        String name = nameField.getText().trim();
        String bloodType = (String) bloodTypeBox.getSelectedItem();
        String unitsText = unitsField.getText().trim();
        String address = addressField.getText().trim();

        if (name.isEmpty() || unitsText.isEmpty() || address.isEmpty()) {
            JOptionPane.showMessageDialog(this, "❌ Please fill in all fields.");
            return;
        }

        try {
            int units = Integer.parseInt(unitsText);
            Connection conn = DriverManager.getConnection(
                    "jdbc:mysql://localhost:3306/dronedb", "root", "Sathishdhana#23"
            );

            String checkQuery = "SELECT quantity_units FROM blood_inventory WHERE blood_type = ?";
            PreparedStatement checkStmt = conn.prepareStatement(checkQuery);
            checkStmt.setString(1, bloodType);
            ResultSet rs = checkStmt.executeQuery();

            if (rs.next()) {
                int available = rs.getInt("quantity_units");
                if (available < units) {
                    JOptionPane.showMessageDialog(this, "❌ Not enough units available. Only " + available + " units left.");
                    conn.close();
                    return;
                }
            }

            String insertQuery = "INSERT INTO delivery_requests (patient_name, blood_type, units_requested, delivery_address) VALUES (?, ?, ?, ?)";
            PreparedStatement insertStmt = conn.prepareStatement(insertQuery);
            insertStmt.setString(1, name);
            insertStmt.setString(2, bloodType);
            insertStmt.setInt(3, units);
            insertStmt.setString(4, address);
            insertStmt.executeUpdate();

            String updateQuery = "UPDATE blood_inventory SET quantity_units = quantity_units - ? WHERE blood_type = ?";
            PreparedStatement updateStmt = conn.prepareStatement(updateQuery);
            updateStmt.setInt(1, units);
            updateStmt.setString(2, bloodType);
            updateStmt.executeUpdate();

            conn.close();

            new ConfirmationPage(name, bloodType, units, address, userPassword);
            dispose();

        } catch (NumberFormatException ex) {
            JOptionPane.showMessageDialog(this, "❌ Units must be a valid number.");
        } catch (SQLException ex) {
            JOptionPane.showMessageDialog(this, "❌ Database error: " + ex.getMessage());
        }
    }
}