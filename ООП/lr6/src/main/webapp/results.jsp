<%@ page contentType="text/html; charset=UTF-8" %>
<!DOCTYPE html>
<html>
<head>
  <title>Temperature Analysis</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
<div class="container mt-5">
  <div class="card shadow">
    <div class="card-header bg-primary text-white">
      <h2 class="text-center">Monthly Temperature Analysis</h2>
    </div>
    <div class="card-body">
      <div class="row">
        <div class="col-md-6">
          <div class="alert alert-info">
            <h4 class="alert-heading">Average Temperature</h4>
            <p class="display-4">${average}°C</p>
          </div>
        </div>

        <div class="col-md-6">
          <div class="alert alert-success">
            <h4 class="alert-heading">Days Above Average</h4>
            <p class="display-4">${above}</p>
          </div>

          <div class="alert alert-warning">
            <h4 class="alert-heading">Days Below Average</h4>
            <p class="display-4">${below}</p>
          </div>
        </div>
      </div>

      <div class="mt-4">
        <h3 class="text-center mb-3">Top 3 Warmest Days</h3>
        <ul class="list-group">
          <li class="list-group-item d-flex justify-content-between align-items-center">
            Day 1
            <span class="badge bg-danger rounded-pill">${top3[0]}</span>
          </li>
          <li class="list-group-item d-flex justify-content-between align-items-center">
            Day 2
            <span class="badge bg-danger rounded-pill">${top3[1]}</span>
          </li>
          <li class="list-group-item d-flex justify-content-between align-items-center">
            Day 3
            <span class="badge bg-danger rounded-pill">${top3[2]}</span>
          </li>
        </ul>
      </div>
    </div>
  </div>
</div>
</body>
</html>