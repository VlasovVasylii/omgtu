package model;

public class Task {
    private String title;
    private String description;
    private String category;
    private String dueDate;
    private String priority;

    public Task(String title, String description, String category, String dueDate, String priority) {
        this.title = title;
        this.description = description;
        this.category = category;
        this.dueDate = dueDate;
        this.priority = priority;
    }

    public String getTitle() {
        return title;
    }

    public String getDescription() {
        return description;
    }

    public String getCategory() {
        return category;
    }

    public String getDueDate() {
        return dueDate;
    }

    public String getPriority() {
        return priority;
    }
}