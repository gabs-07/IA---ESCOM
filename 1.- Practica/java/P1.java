package p1;

import javax.swing.*;
import java.awt.Color;
import java.awt.Font;
import java.awt.BorderLayout;
import java.util.HashSet;
import java.util.Set;
import java.util.ArrayList;
import java.util.List;

public class P1 {

    private static final int[] persona = {1, 2, 5, 10};
    private static JTextArea textResult;

    // Función que imprime el título
    private static String imprimirTitulo() {
        return "\n Practica Uno: The bridge and torch problem \n";
    }

    // Función que encuentra el tiempo óptimo
    private static List<Solucion> timeOptimo(int[] persona) {
        Set<Integer> izqInicial = new HashSet<>();
        for (int p : persona) izqInicial.add(p);

        List<Solucion> soluciones = new ArrayList<>();
        int[] mejorTiempo = {Integer.MAX_VALUE};

        dfs(new HashSet<>(izqInicial), new HashSet<>(), 0, "izq", new ArrayList<>(), soluciones, mejorTiempo);

        return soluciones;
    }

    private static void dfs(Set<Integer> izq, Set<Integer> der, int tiempo, String antorcha,
                            List<String> camino, List<Solucion> soluciones, int[] mejorTiempo) {
        if (tiempo >= mejorTiempo[0]) return;

        if (izq.isEmpty()) {
            if (tiempo < mejorTiempo[0]) {
                mejorTiempo[0] = tiempo;
                soluciones.clear();
                soluciones.add(new Solucion(tiempo, new ArrayList<>(camino)));
            } else if (tiempo == mejorTiempo[0]) {
                soluciones.add(new Solucion(tiempo, new ArrayList<>(camino)));
            }
            return;
        }

        if (antorcha.equals("izq")) {
            List<Integer> listaIzq = new ArrayList<>(izq);
            for (int i = 0; i < listaIzq.size(); i++) {
                for (int j = i + 1; j < listaIzq.size(); j++) {
                    int a = listaIzq.get(i);
                    int b = listaIzq.get(j);

                    int nuevoTiempo = tiempo + Math.max(a, b);

                    Set<Integer> nuevoIzq = new HashSet<>(izq);
                    nuevoIzq.remove(a);
                    nuevoIzq.remove(b);

                    Set<Integer> nuevoDer = new HashSet<>(der);
                    nuevoDer.add(a);
                    nuevoDer.add(b);

                    List<String> nuevoCamino = new ArrayList<>(camino);
                    nuevoCamino.add(a + "," + b + " → (" + Math.max(a, b) + ")");

                    dfs(nuevoIzq, nuevoDer, nuevoTiempo, "der", nuevoCamino, soluciones, mejorTiempo);
                }
            }
        } else {
            for (int a : new ArrayList<>(der)) {
                int nuevoTiempo = tiempo + a;

                Set<Integer> nuevoIzq = new HashSet<>(izq);
                nuevoIzq.add(a);

                Set<Integer> nuevoDer = new HashSet<>(der);
                nuevoDer.remove(a);

                List<String> nuevoCamino = new ArrayList<>(camino);
                nuevoCamino.add(a + " ← (" + a + ")");

                dfs(nuevoIzq, nuevoDer, nuevoTiempo, "izq", nuevoCamino, soluciones, mejorTiempo);
            }
        }
    }

    // Clase para guardar soluciones
    private static class Solucion {
        int tiempo;
        List<String> pasos;

        Solucion(int tiempo, List<String> pasos) {
            this.tiempo = tiempo;
            this.pasos = pasos;
        }
    }

    // Función que imprime los resultados en el JTextArea
    private static void imprimirResultados() {
        List<Solucion> soluciones = timeOptimo(persona);

        textResult.setText(""); // limpiar antes de escribir
        textResult.append(imprimirTitulo());
        textResult.append("Mejor tiempo: " + soluciones.get(0).tiempo + " minutos\n\n");
        textResult.append("Una de las soluciones óptimas:\n");
        for (String paso : soluciones.get(0).pasos) {
            textResult.append("  " + paso + "\n");
        }
    }

    // Ventana principal
    public static void main(String[] args) {
        JFrame ventana = new JFrame("The Bridge and Torch Problem");
        ventana.setSize(500, 400);
        ventana.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        ventana.setLayout(new BorderLayout());

        JLabel labelTitle = new JLabel("Practica Uno: The Bridge and Torch Problem", JLabel.CENTER);
        labelTitle.setFont(new Font("Arial", Font.BOLD, 14));
        ventana.add(labelTitle, BorderLayout.NORTH);

        JButton btnRun = new JButton("Resolver");
        btnRun.setFont(new Font("Arial", Font.PLAIN, 12));
        btnRun.setBackground(Color.RED);
        btnRun.setForeground(Color.WHITE);
        btnRun.addActionListener(e -> imprimirResultados());
        ventana.add(btnRun, BorderLayout.SOUTH);

        textResult = new JTextArea();
        textResult.setFont(new Font("Consolas", Font.PLAIN, 11));
        textResult.setWrapStyleWord(true);
        textResult.setLineWrap(true);

        JScrollPane scroll = new JScrollPane(textResult);
        ventana.add(scroll, BorderLayout.CENTER);

        ventana.setVisible(true);
    }
}
