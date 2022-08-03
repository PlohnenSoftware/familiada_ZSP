import java.awt.*;
import javax.swing.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.font.*;
import java.util.HashMap;
import java.util.Map;
import java.awt.event.*;


public class Main extends JFrame implements ActionListener {

    public JButton I;
    public JButton II;
    public JButton III;
    public JButton IV;
    public JButton V;
    public JButton VI;
    public JButton poka;


    public Graphics2D napisy1;
    public Graphics2D napisy2;
    public Graphics2D napisy3;
    public Graphics2D napisy4;
    public Graphics2D napisy5;
    public Graphics2D napisy6;
    public Graphics2D napiss;


    public JTextField final1;
    public JTextField final2;
    public JTextField final3;
    public JTextField final4;
    public JTextField final5;
    public JTextField final21;
    public JTextField final22;
    public JTextField final23;
    public JTextField final24;
    public JTextField final25;
    public JTextField pkform1;
    public JTextField pkform2;
    public JTextField pkform3;
    public JTextField pkform4;
    public JTextField pkform5;
    public JTextField pkform21;
    public JTextField pkform22;
    public JTextField pkform23;
    public JTextField pkform24;
    public JTextField pkform25;
    public JTextField nauczyciele;
    public JTextField uczniowie;


    JFrame frame = new JFrame("FAMILIADA");
    JFrame frame3 = new JFrame("napisy");

    int h;
    int w;
    boolean pierwszy;
    boolean pkt1, pkt2, pkt3, pkt4, pkt5, pkt6, fin1, fin2, fin3, fin4, fin5, fin21, fin22, fin23, fin24, fin25, szansald, szansal1, szansal2, szansal3, szansapd, szansap1, szansap2, szansap3;
    public int pk1 = 0, pk2, pk3, pk4, pk5, pk6, runda;
    public int suma = 0;

    String haslo1 = "1~~~~~~~~~~~~~~~~~~~~";
    String haslo2 = "2~~~~~~~~~~~~~~~~~~~~";
    String haslo3 = "3~~~~~~~~~~~~~~~~~~~~";
    String haslo4 = "4~~~~~~~~~~~~~~~~~~~~";
    String haslo5 = "5~~~~~~~~~~~~~~~~~~~~";
    String haslo6 = "6~~~~~~~~~~~~~~~~~~~~";

    String fhaslo1 = "~~~~~~~~~~";
    String fhaslo2 = "~~~~~~~~~~";
    String fhaslo3 = "~~~~~~~~~~";
    String fhaslo4 = "~~~~~~~~~~";
    String fhaslo5 = "~~~~~~~~~~";
    String fhaslo21 = "~~~~~~~~~~";
    String fhaslo22 = "~~~~~~~~~~";
    String fhaslo23 = "~~~~~~~~~~";
    String fhaslo24 = "~~~~~~~~~~";
    String fhaslo25 = "~~~~~~~~~~";

    String fpkt1, fpkt2, fpkt3, fpkt4, fpkt5, fpkt21, fpkt22, fpkt23, fpkt24, fpkt25;

    String wysw_pkt1, wysw_pkt2;

    int[] punkt1 = {30, 25, 29, 30, 32};
    int[] punkt2 = {20, 16, 23, 16, 23};
    int[] punkt3 = {12, 15, 20, 15, 14};
    int[] punkt4 = {11, 11, 9, 14, 10};
    int[] punkt5 = {11, 8, 8, 12, 5};
    int[] punkt6 = {10, 7, 2, 5, 4};

    int punkty_druzyna1;
    int punkty_druzyna2;

    String[] haslo11 = {"CHORWACJA", "NAUCZYĆ SIĘ", "MILIONERZY", "FRANCUSKI", "BIEGUN"};
    String[] haslo22 = {"GRECJA", "W PIÓRNIKU", "FAMILIADA", "HISZPAŃSKI", "KOREA"};
    String[] haslo33 = {"TURCJA", "W RĘKAWIE", "1 Z 10", "WŁOSKI", "PÓŁKULA"};
    String[] haslo44 = {"WŁOCHY", "POZA/NAUCZYCIELA", "JAKA TO MELODIA", "ANGIELSKI", "WIATR"};
    String[] haslo55 = {"HISZPANIA", "TELEFON", "KOŁO FORTUNY", "NIEMIECKI", "AMERYKA"};
    String[] haslo66 = {"BUŁGARIA", "W DŁUGOPISIE", "KOCHAM CIĘ POLSKI", "JAPOŃSKI", "MORZE"};

    public static void main(String[] args){
        Main funk =new Main();
        funk.run();
    }

    public void run() {
        JFrame frame2 = new JFrame("STEROWANIE");
        frame3.setSize(700, 300);
        frame.add(new TestPane());
        frame.pack();
        frame.setLocationRelativeTo(null);
        frame.setExtendedState(JFrame.MAXIMIZED_BOTH);
        frame.setVisible(true);
        frame.getSize();
        Rectangle r = frame.getBounds();
        h = r.height;
        w = r.width;
        //frame2.add(new TestPane1());
        frame2.pack();
        frame2.setSize(800, 600);
        I = new JButton("1 hasło");
        I.setBounds(50, 50, 95, 30);
        I.addActionListener(this);
        frame2.add(I);
        II = new JButton("2 hasło");
        II.setBounds(50, 100, 95, 30);
        II.addActionListener(this);
        frame2.add(II);
        III = new JButton("3 hasło");
        III.setBounds(50, 150, 95, 30);
        III.addActionListener(this);
        frame2.add(III);
        IV = new JButton("4 hasło");
        IV.setBounds(50, 200, 95, 30);
        IV.addActionListener(this);
        frame2.add(IV);
        V = new JButton("5 hasło");
        V.setBounds(50, 250, 95, 30);
        V.addActionListener(this);
        frame2.add(V);
        VI = new JButton("6 hasło");
        VI.setBounds(50, 300, 95, 30);
        VI.addActionListener(this);
        frame2.add(VI);
        poka = new JButton("Pokaż punkty");
        poka.setBounds(650, 10, 95, 30);
        poka.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                wysw_pkt1 = uczniowie.getText();
                wysw_pkt2 = nauczyciele.getText();
                runda = 7;
                frame.repaint();
            }
        });
        frame2.add(poka);
        JButton round1 = new JButton("1 runda");
        JButton round2 = new JButton("2 runda");
        JButton round3 = new JButton("3 runda");
        JButton round4 = new JButton("4 runda");
        JButton round5 = new JButton("5 runda");
        JButton finnal = new JButton("finał");
        round1.setBounds(50, 10, 95, 30);
        round2.setBounds(150, 10, 95, 30);
        round3.setBounds(250, 10, 95, 30);
        round4.setBounds(350, 10, 95, 30);
        round5.setBounds(450, 10, 95, 30);
        finnal.setBounds(550, 10, 95, 30);
        round1.addActionListener(this);
        round2.addActionListener(this);
        round3.addActionListener(this);
        round4.addActionListener(this);
        round5.addActionListener(this);
        finnal.addActionListener(this);
        frame2.add(round1);
        frame2.add(round2);
        frame2.add(round3);
        frame2.add(round4);
        frame2.add(round5);
        frame2.add(finnal);
        JButton szansaldu = new JButton("Szansa duża lewa");
        JButton szansal11 = new JButton("Szansa lewa 1");
        JButton szansal22 = new JButton("Szansa lewa 2");
        JButton szansal33 = new JButton("Szansa lewa 3");
        JButton szansapdu = new JButton("Szansa duża prawa");
        JButton szansap11 = new JButton("Szansa prawa 1");
        JButton szansap22 = new JButton("Szansa prawa 2");
        JButton szansap33 = new JButton("Szansa prawa 3");
        szansaldu.setBounds(200, 70, 200, 30);
        szansal11.setBounds(200, 105, 200, 30);
        szansal22.setBounds(200, 140, 200, 30);
        szansal33.setBounds(200, 175, 200, 30);
        szansapdu.setBounds(405, 70, 200, 30);
        szansap11.setBounds(405, 105, 200, 30);
        szansap22.setBounds(405, 140, 200, 30);
        szansap33.setBounds(405, 175, 200, 30);
        szansaldu.addActionListener(this);
        szansal11.addActionListener(this);
        szansal22.addActionListener(this);
        szansal33.addActionListener(this);
        szansapdu.addActionListener(this);
        szansap11.addActionListener(this);
        szansap22.addActionListener(this);
        szansap33.addActionListener(this);
        frame2.add(szansaldu);
        frame2.add(szansal11);
        frame2.add(szansal22);
        frame2.add(szansal33);
        frame2.add(szansapdu);
        frame2.add(szansap11);
        frame2.add(szansap22);
        frame2.add(szansap33);
        JButton druzyna1 = new JButton("Dodaj do 1");
        JButton druzyna2 = new JButton("Dodaj do 2");
        druzyna1.setBounds(25, 350, 95, 30);
        druzyna2.setBounds(130, 350, 95, 30);
        druzyna1.addActionListener(this);
        druzyna2.addActionListener(this);
        frame2.add(druzyna1);
        frame2.add(druzyna2);
        frame2.setLocationRelativeTo(null);
        frame2.setLayout(null);
        frame2.setVisible(true);
        JTextField final1 = new JTextField();
        JTextField final2 = new JTextField();
        JTextField final3 = new JTextField();
        JTextField final4 = new JTextField();
        JTextField final5 = new JTextField();
        JTextField final21 = new JTextField();
        JTextField final22 = new JTextField();
        JTextField final23 = new JTextField();
        JTextField final24 = new JTextField();
        JTextField final25 = new JTextField();
        JTextField pkform1 = new JTextField();
        JTextField pkform2 = new JTextField();
        JTextField pkform3 = new JTextField();
        JTextField pkform4 = new JTextField();
        JTextField pkform5 = new JTextField();
        JTextField pkform21 = new JTextField();
        JTextField pkform22 = new JTextField();
        JTextField pkform23 = new JTextField();
        JTextField pkform24 = new JTextField();
        JTextField pkform25 = new JTextField();
        uczniowie = new JTextField();
        nauczyciele = new JTextField();
        final1.setBounds(10, 10, 90, 30);
        final2.setBounds(10, 50, 90, 30);
        final3.setBounds(10, 90, 90, 30);
        final4.setBounds(10, 130, 90, 30);
        final5.setBounds(10, 170, 90, 30);
        final21.setBounds(295, 10, 90, 30);
        final22.setBounds(295, 50, 90, 30);
        final23.setBounds(295, 90, 90, 30);
        final24.setBounds(295, 130, 90, 30);
        final25.setBounds(295, 170, 90, 30);
        pkform1.setBounds(105, 10, 90, 30);
        pkform2.setBounds(105, 50, 90, 30);
        pkform3.setBounds(105, 90, 90, 30);
        pkform4.setBounds(105, 130, 90, 30);
        pkform5.setBounds(105, 170, 90, 30);
        pkform21.setBounds(390, 10, 90, 30);
        pkform22.setBounds(390, 50, 90, 30);
        pkform23.setBounds(390, 90, 90, 30);
        pkform24.setBounds(390, 130, 90, 30);
        pkform25.setBounds(390, 170, 90, 30);
        uczniowie.setBounds(10, 210, 90, 30);
        nauczyciele.setBounds(200, 210, 90, 30);
        frame3.add(final1);
        frame3.add(final2);
        frame3.add(final3);
        frame3.add(final4);
        frame3.add(final5);
        frame3.add(final21);
        frame3.add(final22);
        frame3.add(final23);
        frame3.add(final24);
        frame3.add(final25);
        frame3.add(pkform1);
        frame3.add(pkform2);
        frame3.add(pkform3);
        frame3.add(pkform4);
        frame3.add(pkform5);
        frame3.add(pkform21);
        frame3.add(pkform22);
        frame3.add(pkform23);
        frame3.add(pkform24);
        frame3.add(pkform25);
        frame3.add(uczniowie);
        frame3.add(nauczyciele);
        JButton akc1 = new JButton("pokaż1");
        JButton akc2 = new JButton("pokaż2");
        JButton akc3 = new JButton("pokaż3");
        JButton akc4 = new JButton("pokaż4");
        JButton akc5 = new JButton("pokaż5");
        JButton akc21 = new JButton("pokaż21");
        JButton akc22 = new JButton("pokaż22");
        JButton akc23 = new JButton("pokaż23");
        JButton akc24 = new JButton("pokaż24");
        JButton akc25 = new JButton("pokaż25");
        akc1.setBounds(200, 10, 90, 30);
        akc2.setBounds(200, 50, 90, 30);
        akc3.setBounds(200, 90, 90, 30);
        akc4.setBounds(200, 130, 90, 30);
        akc5.setBounds(200, 170, 90, 30);
        akc21.setBounds(480, 10, 90, 30);
        akc22.setBounds(480, 50, 90, 30);
        akc23.setBounds(480, 90, 90, 30);
        akc24.setBounds(480, 130, 90, 30);
        akc25.setBounds(480, 170, 90, 30);
        akc1.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent e){
                fhaslo1 = final1.getText();
                fpkt1 = pkform1.getText();
                fin1 = true;
                suma = suma + Integer.parseInt(fpkt1);
                frame.repaint();
            }
        });
        akc2.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent e){
                fhaslo2 = final2.getText();
                fpkt2 = pkform2.getText();
                fin2 = true;
                suma = suma + Integer.parseInt(fpkt2);
                frame.repaint();
            }
        });
        akc3.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent e){
                fhaslo3 = final3.getText();
                fpkt3 = pkform3.getText();
                fin3 = true;
                suma = suma + Integer.parseInt(fpkt3);
                frame.repaint();
            }
        });
        akc4.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent e){
                fhaslo4 = final4.getText();
                fpkt4 = pkform4.getText();
                fin4 = true;
                suma = suma + Integer.parseInt(fpkt4);
                frame.repaint();
            }
        });
        akc5.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent e){
                fhaslo5 = final5.getText();
                fpkt5 = pkform5.getText();
                fin5 = true;
                suma = suma + Integer.parseInt(fpkt5);
                frame.repaint();
            }
        });
        akc21.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent e){
                fhaslo21 = final21.getText();
                fpkt21 = pkform21.getText();
                fin21 = true;
                suma = suma + Integer.parseInt(fpkt21);
                frame.repaint();
            }
        });
        akc22.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent e){
                fhaslo22 = final22.getText();
                fpkt22 = pkform22.getText();
                fin22 = true;
                suma = suma + Integer.parseInt(fpkt22);
                frame.repaint();
            }
        });
        akc23.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent e){
                fhaslo23 = final23.getText();
                fpkt23 = pkform23.getText();
                fin23 = true;
                suma = suma + Integer.parseInt(fpkt23);
                frame.repaint();
            }
        });
        akc24.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent e){
                fhaslo24 = final24.getText();
                fpkt24 = pkform24.getText();
                fin24 = true;
                suma = suma + Integer.parseInt(fpkt24);
                frame.repaint();
            }
        });
        akc25.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent e){
                fhaslo25 = final25.getText();
                fpkt25 = pkform25.getText();
                fin25 = true;
                suma = suma + Integer.parseInt(fpkt25);
                frame.repaint();
            }
        });
        frame3.add(akc1);
        frame3.add(akc2);
        frame3.add(akc3);
        frame3.add(akc4);
        frame3.add(akc5);
        frame3.add(akc21);
        frame3.add(akc22);
        frame3.add(akc23);
        frame3.add(akc24);
        frame3.add(akc25);
        if(fin1) fhaslo1 = final1.getText();
        frame3.setLayout(null);
        frame3.setVisible(true);
    }



    public class TestPane extends JPanel {
        public TestPane() {
            setBackground(Color.BLACK);
        }

        @Override
        public Dimension getPreferredSize() {
            return new Dimension(1920, 1080);
        }

        @Override
        protected void paintComponent(Graphics g) {
            super.paintComponent(g);
            Graphics2D aroundframe = (Graphics2D) g.create();
            Graphics2D insidebox = (Graphics2D) g.create();
            Graphics2D smallboxes = (Graphics2D) g.create();
            Graphics2D napisy = (Graphics2D) g.create();
            Graphics2D szanse = (Graphics2D) g.create();
                napisy1 = (Graphics2D) g.create();
                napisy2 = (Graphics2D) g.create();
                napisy3 = (Graphics2D) g.create();
                napisy4 = (Graphics2D) g.create();
                napisy5 = (Graphics2D) g.create();
                napisy6 = (Graphics2D) g.create();
                napiss = (Graphics2D) g.create();
                aroundframe.setPaint(Color.BLUE);
                aroundframe.fillRect(0, 0, 1920, 1080);
                aroundframe.dispose();
                insidebox.setPaint(Color.GRAY);
                insidebox.fillRect(35, 15, w - 75, h - 65);
                smallboxes.setPaint(Color.DARK_GRAY);
                for (int i = 1; i <= 29; i++) {
                    for (int j = 1; j <= 11; j++) {
                        smallboxes.fillRect(50 * i, 70 * j - 40, 45, 65);
                    }
                }
                smallboxes.dispose();
                napisy.setPaint(Color.YELLOW);
                Font font = new Font("Consolas", Font.PLAIN, 40);
                Map<TextAttribute, Object> attributes = new HashMap<TextAttribute, Object>();
                attributes.put(TextAttribute.TRACKING, 0.705);
                Font font2 = font.deriveFont(attributes);
                napisy.setFont(font2);
            napiss.setPaint(Color.YELLOW);
            napiss.setFont(font2);
            if(runda != 6 && runda != 7) {
                napisy1.setPaint(Color.YELLOW);
                napisy2.setPaint(Color.YELLOW);
                napisy3.setPaint(Color.YELLOW);
                napisy4.setPaint(Color.YELLOW);
                napisy5.setPaint(Color.YELLOW);
                napisy6.setPaint(Color.YELLOW);
                napisy1.setFont(font2);
                napisy2.setFont(font2);
                napisy3.setFont(font2);
                napisy4.setFont(font2);
                napisy5.setFont(font2);
                napisy6.setFont(font2);
                napiss.setFont(font2);
                napisy1.drawString(haslo1, 215, 220);
                if (pkt1) napisy1.drawString(String.valueOf(pk1), 1260, 220);
                napisy2.drawString(haslo2, 215, 290);
                if (pkt2) napisy2.drawString(String.valueOf(pk2), 1260, 290);
                napisy3.drawString(haslo3, 215, 360);
                if (pkt3) napisy3.drawString(String.valueOf(pk3), 1260, 360);
                if (haslo4.equals("4.POZA ZASIĘGIEM WZROKU NAUCZYCIELA")) {
                    napisy4.drawString("4.POZA ZASIĘGIEM WZROKU", 465, 430);
                    napisy4.drawString("NAUCZYCIELA", 215, 430);
                } else {
                    napisy4.drawString(haslo4, 215, 430);
                }
                if (pkt4) napisy4.drawString(String.valueOf(pk4), 1260, 430);
                napisy5.drawString(haslo5, 215, 500);
                if (pkt5) napisy5.drawString(String.valueOf(pk5), 1260, 500);
                napisy6.drawString(haslo6, 215, 570);
                if (pkt6) napisy6.drawString(String.valueOf(pk6), 1260, 570);
                napiss.drawString("SUMA", 910, 640);
                napiss.drawString(String.valueOf(suma), 1260, 640);
                napisy1.dispose();
                napisy2.dispose();
                napisy3.dispose();
                napisy4.dispose();
                napisy6.dispose();
                napiss.dispose();
                szanse.setPaint(Color.YELLOW);
                if(szansal1){
                    szanse.fillRect(50, 30, 45, 65);
                    szanse.fillRect(150, 30, 45, 65);
                    szanse.fillRect(100, 100, 45, 65);
                    szanse.fillRect(50, 170, 45, 65);
                    szanse.fillRect(150, 170, 45, 65);
                }
                if(szansal2){
                    szanse.fillRect(50, 310, 45, 65);
                    szanse.fillRect(150, 310, 45, 65);
                    szanse.fillRect(100, 380, 45, 65);
                    szanse.fillRect(50, 450, 45, 65);
                    szanse.fillRect(150, 450, 45, 65);
                }
                if(szansal3){
                    szanse.fillRect(50, 590, 45, 65);
                    szanse.fillRect(150, 590, 45, 65);
                    szanse.fillRect(100, 660, 45, 65);
                    szanse.fillRect(50, 730, 45, 65);
                    szanse.fillRect(150, 730, 45, 65);
                }
                if(szansald){
                    szanse.fillRect(50, 170, 45, 65);
                    szanse.fillRect(150, 170, 45, 65);
                    szanse.fillRect(50, 240, 45, 65);
                    szanse.fillRect(150, 240, 45, 65);
                    szanse.fillRect(100, 310, 45, 65);
                    szanse.fillRect(100, 380, 45, 65);
                    szanse.fillRect(100, 450, 45, 65);
                    szanse.fillRect(50, 520, 45, 65);
                    szanse.fillRect(150, 520, 45, 65);
                    szanse.fillRect(50, 590, 45, 65);
                    szanse.fillRect(150, 590, 45, 65);
                }
                if(szansap1){
                    szanse.fillRect(1350, 30, 45, 65);
                    szanse.fillRect(1450, 30, 45, 65);
                    szanse.fillRect(1400, 100, 45, 65);
                    szanse.fillRect(1350, 170, 45, 65);
                    szanse.fillRect(1450, 170, 45, 65);
                }
                if(szansap2){
                    szanse.fillRect(1350, 310, 45, 65);
                    szanse.fillRect(1450, 310, 45, 65);
                    szanse.fillRect(1400, 380, 45, 65);
                    szanse.fillRect(1350, 450, 45, 65);
                    szanse.fillRect(1450, 450, 45, 65);
                }
                if(szansap3){
                    szanse.fillRect(1350, 590, 45, 65);
                    szanse.fillRect(1450, 590, 45, 65);
                    szanse.fillRect(1400, 660, 45, 65);
                    szanse.fillRect(1350, 730, 45, 65);
                    szanse.fillRect(1450, 730, 45, 65);
                }
                if(szansapd){
                    szanse.fillRect(1350, 170, 45, 65);
                    szanse.fillRect(1450, 170, 45, 65);
                    szanse.fillRect(1350, 240, 45, 65);
                    szanse.fillRect(1450, 240, 45, 65);
                    szanse.fillRect(1400, 310, 45, 65);
                    szanse.fillRect(1400, 380, 45, 65);
                    szanse.fillRect(1400, 450, 45, 65);
                    szanse.fillRect(1350, 520, 45, 65);
                    szanse.fillRect(1450, 520, 45, 65);
                    szanse.fillRect(1350, 590, 45, 65);
                    szanse.fillRect(1450, 590, 45, 65);
                }
                szanse.dispose();
            }
            if(runda == 6){
                napiss.drawString("SUMA", 910, 640);
                napiss.drawString(String.valueOf(suma), 1260, 640);
                Graphics2D finalhaslo1 = (Graphics2D) g.create();
                Graphics2D finalhaslo2 = (Graphics2D) g.create();
                Graphics2D finalhaslo3 = (Graphics2D) g.create();
                Graphics2D finalhaslo4 = (Graphics2D) g.create();
                Graphics2D finalhaslo5 = (Graphics2D) g.create();
                Graphics2D finalhaslo21 = (Graphics2D) g.create();
                Graphics2D finalhaslo22 = (Graphics2D) g.create();
                Graphics2D finalhaslo23 = (Graphics2D) g.create();
                Graphics2D finalhaslo24 = (Graphics2D) g.create();
                Graphics2D finalhaslo25 = (Graphics2D) g.create();
                finalhaslo1.setPaint(Color.YELLOW);
                finalhaslo2.setPaint(Color.YELLOW);
                finalhaslo3.setPaint(Color.YELLOW);
                finalhaslo4.setPaint(Color.YELLOW);
                finalhaslo5.setPaint(Color.YELLOW);
                finalhaslo21.setPaint(Color.YELLOW);
                finalhaslo22.setPaint(Color.YELLOW);
                finalhaslo23.setPaint(Color.YELLOW);
                finalhaslo24.setPaint(Color.YELLOW);
                finalhaslo25.setPaint(Color.YELLOW);
                finalhaslo1.setFont(font2);
                finalhaslo2.setFont(font2);
                finalhaslo3.setFont(font2);
                finalhaslo4.setFont(font2);
                finalhaslo5.setFont(font2);
                finalhaslo21.setFont(font2);
                finalhaslo22.setFont(font2);
                finalhaslo23.setFont(font2);
                finalhaslo24.setFont(font2);
                finalhaslo25.setFont(font2);
                finalhaslo1.drawString(fhaslo1, 115, 220);
                if(fin1) finalhaslo1.drawString(fpkt1, 665, 220);
                finalhaslo2.drawString(fhaslo2, 115, 290);
                if(fin2) finalhaslo2.drawString(fpkt2, 665, 290);
                finalhaslo3.drawString(fhaslo3, 115, 360);
                if(fin3) finalhaslo2.drawString(fpkt3, 665, 360);
                finalhaslo4.drawString(fhaslo4, 115, 430);
                if(fin4) finalhaslo2.drawString(fpkt4, 665, 430);
                finalhaslo5.drawString(fhaslo5, 115, 500);
                if(fin5) finalhaslo2.drawString(fpkt5, 665, 500);
                finalhaslo21.drawString(fhaslo21, 965, 220);
                if(fin21) finalhaslo2.drawString(fpkt21, 815, 220);
                finalhaslo22.drawString(fhaslo22, 965, 290);
                if(fin22) finalhaslo2.drawString(fpkt22, 815, 290);
                finalhaslo23.drawString(fhaslo23, 965, 360);
                if(fin23) finalhaslo2.drawString(fpkt23, 815, 360);
                finalhaslo24.drawString(fhaslo24, 965, 430);
                if(fin24) finalhaslo2.drawString(fpkt24, 815, 430);
                finalhaslo25.drawString(fhaslo25, 965,  500);
                if(fin25) finalhaslo2.drawString(fpkt25, 815, 500);
                finalhaslo1.dispose();
                finalhaslo2.dispose();
                finalhaslo3.dispose();
                finalhaslo4.dispose();
                finalhaslo5.dispose();
                finalhaslo21.dispose();
                finalhaslo22.dispose();
                finalhaslo23.dispose();
                finalhaslo24.dispose();
                finalhaslo25.dispose();
                napiss.dispose();
            }
            if(runda == 7){
                Graphics2D punktyuczn = (Graphics2D) g.create();
                Graphics2D punktynauc = (Graphics2D) g.create();
                punktyuczn.setPaint(Color.YELLOW);
                punktynauc.setPaint(Color.YELLOW);
                punktyuczn.setFont(font2);
                punktynauc.setFont(font2);
                punktyuczn.drawString("UCZNIOWIE", 260,290);
                punktyuczn.drawString(wysw_pkt1, 410, 430);
                punktynauc.drawString("NAUCZYCIELE", 810,290);
                punktynauc.drawString(wysw_pkt2, 1010,430);
                punktyuczn.dispose();
                punktynauc.dispose();
            }
        }
    }

    public void actionPerformed(ActionEvent e){
        Graphics g;
        if(e.getActionCommand().equals("1 hasło")){
            haslo1 = "1."+haslo11[runda-1];
            pk1 = punkt1[runda-1];
            pkt1 = true;
            suma = suma + punkt1[runda-1];
            frame.repaint();
        }
        if(e.getActionCommand().equals("2 hasło")){
            haslo2 = "2."+haslo22[runda-1];
            pk2 = punkt2[runda-1];
            pkt2 = true;
            suma = suma + punkt2[runda-1];
            frame.repaint();
        }
        if(e.getActionCommand().equals("3 hasło")){
            haslo3 = "3."+haslo33[runda-1];
            pk3 = punkt3[runda-1];
            pkt3 = true;
            suma = suma + punkt3[runda-1];
            frame.repaint();
        }
        if(e.getActionCommand().equals("4 hasło")){
            haslo4 = "4."+haslo44[runda-1];
            pk4 = punkt4[runda-1];
            pkt4 = true;
            suma = suma + punkt4[runda-1];
            frame.repaint();
        }
        if(e.getActionCommand().equals("5 hasło")){
            haslo5 = "5."+haslo55[runda-1];
            pk5 = punkt5[runda-1];
            pkt5 = true;
            suma = suma + punkt5[runda-1];
            frame.repaint();
        }
        if(e.getActionCommand().equals("6 hasło")){
            haslo6 = "6."+haslo66[runda-1];
            pk6 = punkt6[runda-1];
            pkt6 = true;
            suma = suma + punkt6[runda-1];
            frame.repaint();
        }
        if(e.getActionCommand().equals("1 runda")){
            runda = 1;
            haslo1 = "1~~~~~~~~~~~~~~~~~~~~";
            haslo2 = "2~~~~~~~~~~~~~~~~~~~~";
            haslo3 = "3~~~~~~~~~~~~~~~~~~~~";
            haslo4 = "4~~~~~~~~~~~~~~~~~~~~";
            haslo5 = "5~~~~~~~~~~~~~~~~~~~~";
            haslo6 = "6~~~~~~~~~~~~~~~~~~~~";
            pkt1 = false; pkt2 = false; pkt3 = false; pkt4 = false; pkt5 = false; pkt6 = false;
            szansald = false; szansal1 = false; szansal2 = false; szansal3 = false; szansapd = false; szansap1 = false; szansap2 = false; szansap3 = false;
            suma = 0;
            frame.repaint();
        }
        if(e.getActionCommand().equals("2 runda")){
            runda = 2;
            haslo1 = "1~~~~~~~~~~~~~~~~~~~~";
            haslo2 = "2~~~~~~~~~~~~~~~~~~~~";
            haslo3 = "3~~~~~~~~~~~~~~~~~~~~";
            haslo4 = "4~~~~~~~~~~~~~~~~~~~~";
            haslo5 = "5~~~~~~~~~~~~~~~~~~~~";
            haslo6 = "6~~~~~~~~~~~~~~~~~~~~";
            pkt1 = false; pkt2 = false; pkt3 = false; pkt4 = false; pkt5 = false; pkt6 = false;
            szansald = false; szansal1 = false; szansal2 = false; szansal3 = false; szansapd = false; szansap1 = false; szansap2 = false; szansap3 = false;
            suma = 0;
            frame.repaint();
        }
        if(e.getActionCommand().equals("3 runda")){
            runda = 3;
            haslo1 = "1~~~~~~~~~~~~~~~~~~~~";
            haslo2 = "2~~~~~~~~~~~~~~~~~~~~";
            haslo3 = "3~~~~~~~~~~~~~~~~~~~~";
            haslo4 = "4~~~~~~~~~~~~~~~~~~~~";
            haslo5 = "5~~~~~~~~~~~~~~~~~~~~";
            haslo6 = "6~~~~~~~~~~~~~~~~~~~~";
            pkt1 = false; pkt2 = false; pkt3 = false; pkt4 = false; pkt5 = false; pkt6 = false;
            szansald = false; szansal1 = false; szansal2 = false; szansal3 = false; szansapd = false; szansap1 = false; szansap2 = false; szansap3 = false;
            suma = 0;
            frame.repaint();
        }
        if(e.getActionCommand().equals("4 runda")){
            runda = 4;
            haslo1 = "1~~~~~~~~~~~~~~~~~~~~";
            haslo2 = "2~~~~~~~~~~~~~~~~~~~~";
            haslo3 = "3~~~~~~~~~~~~~~~~~~~~";
            haslo4 = "4~~~~~~~~~~~~~~~~~~~~";
            haslo5 = "5~~~~~~~~~~~~~~~~~~~~";
            haslo6 = "6~~~~~~~~~~~~~~~~~~~~";
            pkt1 = false; pkt2 = false; pkt3 = false; pkt4 = false; pkt5 = false; pkt6 = false;
            szansald = false; szansal1 = false; szansal2 = false; szansal3 = false; szansapd = false; szansap1 = false; szansap2 = false; szansap3 = false;
            suma = 0;
            frame.repaint();
        }
        if(e.getActionCommand().equals("5 runda")){
            runda = 5;
            haslo1 = "1~~~~~~~~~~~~~~~~~~~~";
            haslo2 = "2~~~~~~~~~~~~~~~~~~~~";
            haslo3 = "3~~~~~~~~~~~~~~~~~~~~";
            haslo4 = "4~~~~~~~~~~~~~~~~~~~~";
            haslo5 = "5~~~~~~~~~~~~~~~~~~~~";
            haslo6 = "6~~~~~~~~~~~~~~~~~~~~";
            pkt1 = false; pkt2 = false; pkt3 = false; pkt4 = false; pkt5 = false; pkt6 = false;
            szansald = false; szansal1 = false; szansal2 = false; szansal3 = false; szansapd = false; szansap1 = false; szansap2 = false; szansap3 = false;
            suma = 0;
            frame.repaint();
        }
        if(e.getActionCommand().equals("finał")){
            runda = 6;
            fhaslo1 = "~~~~~~~~~~";
            fhaslo2 = "~~~~~~~~~~";
            fhaslo3 = "~~~~~~~~~~";
            fhaslo4 = "~~~~~~~~~~";
            fhaslo5 = "~~~~~~~~~~";
            fhaslo21 = "~~~~~~~~~~";
            fhaslo22 = "~~~~~~~~~~";
            fhaslo23 = "~~~~~~~~~~";
            fhaslo24 = "~~~~~~~~~~";
            fhaslo25 = "~~~~~~~~~~";
            suma = 0;
            pkt1 = false; pkt2 = false; pkt3 = false; pkt4 = false; pkt5 = false; pkt6 = false; fin1 = false; fin2 = false; fin3 = false; fin4 = false; fin5 = false; fin21 = false; fin22 = false; fin23 = false; fin24 = false; fin25 = false;
            szansald = false; szansal1 = false; szansal2 = false; szansal3 = false; szansapd = false; szansap1 = false; szansap2 = false; szansap3 = false;
            frame.repaint();
        }
        if(e.getActionCommand().equals("Dodaj do 1")){
            punkty_druzyna1 = punkty_druzyna1 + suma;
            suma = 0;
        }
        if(e.getActionCommand().equals("Dodaj do 2")){
            punkty_druzyna2 = punkty_druzyna2 + suma;
            suma = 0;
        }
        if(e.getActionCommand().equals("Szansa duża lewa")){
            szansald = true;
            frame.repaint();
        }
        if(e.getActionCommand().equals("Szansa lewa 1")){
            szansal1 = true;
            frame.repaint();
        }
        if(e.getActionCommand().equals("Szansa lewa 2")){
            szansal2 = true;
            frame.repaint();
        }
        if(e.getActionCommand().equals("Szansa lewa 3")){
            szansal3 = true;
            frame.repaint();
        }
        if(e.getActionCommand().equals("Szansa duża prawa")){
            szansapd = true;
            frame.repaint();
        }
        if(e.getActionCommand().equals("Szansa prawa 1")){
            szansap1 = true;
            frame.repaint();
        }
        if(e.getActionCommand().equals("Szansa prawa 2")){
            szansap2 = true;
            frame.repaint();
        }
        if(e.getActionCommand().equals("Szansa prawa 3")){
            szansap3 = true;
            frame.repaint();
        }
    }

    public class TestPane1 extends JPanel {

        public TestPane1() {
            setBackground(Color.BLACK);
        }

        @Override
        public Dimension getPreferredSize() {
            return new Dimension(600, 400);
        }

        @Override
        protected void paintComponent(Graphics g) {
            super.paintComponent(g);
           /* Graphics2D aroundframe = (Graphics2D) g.create();
            aroundframe.setPaint(Color.BLUE);
            aroundframe.fillRect(0, 0, 1920, 1080);
            aroundframe.dispose();
            Font font = new Font("serif", Font.PLAIN, 25);
            Map<TextAttribute, Object> attributes = new HashMap<TextAttribute, Object>();
            attributes.put(TextAttribute.TRACKING, 0.587);
            Font font2 = font.deriveFont(attributes);*/
        }
    }

}