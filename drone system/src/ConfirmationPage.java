import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class ConfirmationPage extends JFrame {
    public ConfirmationPage(String name, String bloodType, int units, String address, String userPassword) {
        setTitle("✅ Order Confirmation");
        setSize(400, 300);
        setLocationRelativeTo(null);
        setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        getContentPane().setBackground(new Color(255, 250, 240));
        setLayout(new GridLayout(6, 1, 10, 10));

        JLabel title = new JLabel("Order Placed Successfully!", SwingConstants.CENTER);
        title.setFont(new Font("Verdana", Font.BOLD, 18));
        title.setForeground(new Color(34, 139, 34));
        add(title);

        add(new JLabel("👤 Patient: " + name, SwingConstants.CENTER));
        add(new JLabel("🩸 Blood Type: " + bloodType, SwingConstants.CENTER));
        add(new JLabel("📦 Units: " + units, SwingConstants.CENTER));
        add(new JLabel("📍 Address: " + address, SwingConstants.CENTER));

        JButton dispatchButton = new JButton("🚁 Proceed to Dispatch");
        dispatchButton.setBackground(new Color(70, 130, 180));
        dispatchButton.setForeground(Color.WHITE);
        dispatchButton.setFont(new Font("Arial", Font.BOLD, 14));
        dispatchButton.addActionListener(e -> {
            new DispatchPage(userPassword);
            dispose();
        });
        add(dispatchButton);

        setVisible(true);
    }
}