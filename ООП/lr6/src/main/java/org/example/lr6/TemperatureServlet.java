package org.example.lr6;

import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

@WebServlet("/temperature")
public class TemperatureServlet extends HttpServlet {
    private final List<Double> temperatures = new ArrayList<>();

    @Override
    public void init() throws ServletException {
        try {
            InputStream is = getServletContext().getResourceAsStream("/data/temperatures.txt");
            BufferedReader reader = new BufferedReader(new InputStreamReader(is));
            String line;
            while ((line = reader.readLine()) != null) {
                String[] values = line.split(" ");
                for (String val : values) {
                    temperatures.add(Double.parseDouble(val));
                }
            }
        } catch (Exception e) {
            throw new ServletException("Error reading temperature data", e);
        }
    }

    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        double average = temperatures.stream()
                .mapToDouble(Double::doubleValue)
                .average()
                .orElse(0.0);

        long aboveAverage = temperatures.stream()
                .filter(t -> t > average)
                .count();

        long belowAverage = temperatures.stream()
                .filter(t -> t < average)
                .count();

        List<Double> sortedTemps = new ArrayList<>(temperatures);
        sortedTemps.sort(Collections.reverseOrder()); // сортировка по убыванию
        List<Double> top3 = sortedTemps.subList(0, Math.min(3, sortedTemps.size()));

        request.setAttribute("average", String.format("%.1f", average));
        request.setAttribute("above", aboveAverage);
        request.setAttribute("below", belowAverage);
        request.setAttribute("top3", top3);

        request.getRequestDispatcher("/results.jsp").forward(request, response);
    }
}