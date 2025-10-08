import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.sql.*;

public class LoginPage extends JFrame implements ActionListener {
    JTextField usernameField;
    JPasswordField passwordField;
    JButton loginButton, signupButton;
    JPanel formPanel;

    public LoginPage() {
        setTitle("Drone System Login");
        setSize(500, 350);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLocationRelativeTo(null);
        setLayout(null); // for animation

        // Gradient background
        JPanel background = new JPanel() {
            protected void paintComponent(Graphics g) {
                Graphics2D g2d = (Graphics2D) g;
                GradientPaint gp = new GradientPaint(0, 0, new Color(135, 206, 250), 0, getHeight(), new Color(255, 182, 193));
                g2d.setPaint(gp);
                g2d.fillRect(0, 0, getWidth(), getHeight());
            }
        };
        background.setBounds(0, 0, 500, 350);
        background.setLayout(null);
        add(background);

        // Form panel (animated)
        formPanel = new JPanel(new GridLayout(3, 2, 10, 10));
        formPanel.setOpaque(false);
        formPanel.setBounds(-300, 80, 300, 150); // start off-screen

        JLabel userLabel = new JLabel("Username:");
        userLabel.setFont(new Font("Segoe UI", Font.BOLD, 14));
        formPanel.add(userLabel);

        usernameField = new JTextField();
        formPanel.add(usernameField);

        JLabel passLabel = new JLabel("Password:");
        passLabel.setFont(new Font("Segoe UI", Font.BOLD, 14));
        formPanel.add(passLabel);

        passwordField = new JPasswordField();
        formPanel.add(passwordField);

        loginButton = new JButton("Login");
        loginButton.setBackground(new Color(60, 179, 113));
        loginButton.setForeground(Color.WHITE);
        loginButton.setFont(new Font("Segoe UI", Font.BOLD, 14));
        loginButton.setFocusPainted(false);
        loginButton.addActionListener(this);
        formPanel.add(loginButton);

        signupButton = new JButton("Sign Up");
        signupButton.setBackground(new Color(70, 130, 180));
        signupButton.setForeground(Color.WHITE);
        signupButton.setFont(new Font("Segoe UI", Font.BOLD, 14));
        signupButton.setFocusPainted(false);
        signupButton.addActionListener(e -> new SignupPage());
        formPanel.add(signupButton);

        background.add(formPanel);
        animateForm();

        setVisible(true);
    }

    // Slide-in animation
    private void animateForm() {
        Timer timer = new Timer(5, null);
        timer.addActionListener(e -> {
            int x = formPanel.getX();
            if (x < 100) {
                formPanel.setLocation(x + 5, formPanel.getY());
            } else {
                ((Timer) e.getSource()).stop();
            }
        });
        timer.start();
    }

    public void actionPerformed(ActionEvent e) {
        String username = usernameField.getText();
        String password = String.valueOf(passwordField.getPassword());

        try {
            Connection conn = DriverManager.getConnection(
                    "jdbc:mysql://localhost:3306/dronedb", "root", "Sathishdhana#23"
            );

            String query = "SELECT * FROM users WHERE username=? AND password=?";
            PreparedStatement stmt = conn.prepareStatement(query);
            stmt.setString(1, username);
            stmt.setString(2, password);

            ResultSet rs = stmt.executeQuery();

            if (rs.next()) {
                JOptionPane.showMessageDialog(this, "✅ Login successful!");

                if (username.equals("admin") && password.equals("admin123")) {
                    new AdminPage(); // Launch admin panel
                } else {
                    new DashboardPage(username); // ✅ Pass the username // Launch user dashboard
                }

                dispose(); // Close login window
            }

            conn.close();
        } catch (SQLException ex) {
            JOptionPane.showMessageDialog(this, "❌ Database error: " + ex.getMessage());
        }
    }

    public static void main(String[] args) {
        new LoginPage();
    }
}