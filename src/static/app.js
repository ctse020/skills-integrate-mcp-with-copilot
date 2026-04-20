// Global variables
let currentUser = null;
let currentToken = null;

// DOM elements
const authSection = document.getElementById('auth-section');
const userInfo = document.getElementById('user-info');
const authButtons = document.getElementById('auth-buttons');
const userName = document.getElementById('user-name');
const logoutBtn = document.getElementById('logout-btn');
const loginBtn = document.getElementById('login-btn');
const registerBtn = document.getElementById('register-btn');

// Modal elements
const authModal = document.getElementById('auth-modal');
const loginForm = document.getElementById('login-form-element');
const registerForm = document.getElementById('register-form-element');
const showRegister = document.getElementById('show-register');
const showLogin = document.getElementById('show-login');

// Navigation
const mainNav = document.getElementById('main-nav');
const navActivities = document.getElementById('nav-activities');
const navProjects = document.getElementById('nav-projects');
const navTeams = document.getElementById('nav-teams');
const navAchievements = document.getElementById('nav-achievements');
const navWorkshops = document.getElementById('nav-workshops');
const navResources = document.getElementById('nav-resources');
const navProfile = document.getElementById('nav-profile');

// Sections
const activitiesSection = document.getElementById('activities-section');
const projectsSection = document.getElementById('projects-section');
const teamsSection = document.getElementById('teams-section');
const achievementsSection = document.getElementById('achievements-section');
const workshopsSection = document.getElementById('workshops-section');
const resourcesSection = document.getElementById('resources-section');
const profileSection = document.getElementById('profile-section');

// Content containers
const activitiesList = document.getElementById('activities-list');
const projectsList = document.getElementById('projects-list');
const teamsList = document.getElementById('teams-list');
const achievementsList = document.getElementById('achievements-list');
const workshopsList = document.getElementById('workshops-list');
const resourcesList = document.getElementById('resources-list');
const profileContent = document.getElementById('profile-content');

// Forms
const projectForm = document.getElementById('project-form');
const teamForm = document.getElementById('team-form');
const achievementForm = document.getElementById('achievement-form');
const workshopForm = document.getElementById('workshop-form');
const resourceForm = document.getElementById('resource-form');

// Create elements
const createProject = document.getElementById('create-project');
const createTeam = document.getElementById('create-team');
const createAchievement = document.getElementById('create-achievement');
const createWorkshop = document.getElementById('create-workshop');
const createResource = document.getElementById('create-resource');

// Attendance
const markPresentBtn = document.getElementById('mark-present');
const markAbsentBtn = document.getElementById('mark-absent');
const attendanceStats = document.getElementById('attendance-stats');

// Initialize app
document.addEventListener("DOMContentLoaded", () => {
  setupEventListeners();
  checkAuthStatus();
});

// Setup event listeners
function setupEventListeners() {
  // Auth buttons
  loginBtn.addEventListener('click', () => showAuthModal('login'));
  registerBtn.addEventListener('click', () => showAuthModal('register'));
  logoutBtn.addEventListener('click', logout);

  // Modal
  document.querySelector('.close').addEventListener('click', hideAuthModal);
  showRegister.addEventListener('click', () => switchAuthForm('register'));
  showLogin.addEventListener('click', () => switchAuthForm('login'));

  // Auth forms
  loginForm.addEventListener('submit', handleLogin);
  registerForm.addEventListener('submit', handleRegister);

  // Navigation
  navActivities.addEventListener('click', () => showSection('activities'));
  navProjects.addEventListener('click', () => showSection('projects'));
  navTeams.addEventListener('click', () => showSection('teams'));
  navAchievements.addEventListener('click', () => showSection('achievements'));
  navWorkshops.addEventListener('click', () => showSection('workshops'));
  navResources.addEventListener('click', () => showSection('resources'));
  navProfile.addEventListener('click', () => showSection('profile'));

  // Forms
  projectForm.addEventListener('submit', handleCreateProject);
  teamForm.addEventListener('submit', handleCreateTeam);
  achievementForm.addEventListener('submit', handleCreateAchievement);
  workshopForm.addEventListener('submit', handleCreateWorkshop);
  resourceForm.addEventListener('submit', handleCreateResource);

  // Attendance
  markPresentBtn.addEventListener('click', () => markAttendance(true));
  markAbsentBtn.addEventListener('click', () => markAttendance(false));
}

// Authentication functions
function checkAuthStatus() {
  const token = localStorage.getItem('token');
  if (token) {
    currentToken = token;
    fetchUserProfile();
  } else {
    showAuthButtons();
  }
}

function showAuthButtons() {
  authButtons.classList.remove('hidden');
  userInfo.classList.add('hidden');
  mainNav.classList.add('hidden');
  showSection('activities');
}

function showUserInfo(user) {
  currentUser = user;
  userName.textContent = `${user.first_name} ${user.last_name}`;
  authButtons.classList.add('hidden');
  userInfo.classList.remove('hidden');
  mainNav.classList.remove('hidden');
  showSection('activities');
}

function showAuthModal(formType) {
  authModal.classList.remove('hidden');
  if (formType === 'login') {
    loginForm.parentElement.classList.remove('hidden');
    registerForm.parentElement.classList.add('hidden');
  } else {
    registerForm.parentElement.classList.remove('hidden');
    loginForm.parentElement.classList.add('hidden');
  }
}

function hideAuthModal() {
  authModal.classList.add('hidden');
}

function switchAuthForm(formType) {
  if (formType === 'register') {
    loginForm.parentElement.classList.add('hidden');
    registerForm.parentElement.classList.remove('hidden');
  } else {
    registerForm.parentElement.classList.add('hidden');
    loginForm.parentElement.classList.remove('hidden');
  }
}

async function handleLogin(event) {
  event.preventDefault();
  const username = document.getElementById('login-username').value;
  const password = document.getElementById('login-password').value;

  try {
    const response = await fetch('/token', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: new URLSearchParams({
        username: username,
        password: password,
      }),
    });

    const data = await response.json();
    if (response.ok) {
      currentToken = data.access_token;
      localStorage.setItem('token', currentToken);
      hideAuthModal();
      fetchUserProfile();
      showMessage('Login successful!', 'success');
    } else {
      showMessage(data.detail || 'Login failed', 'error');
    }
  } catch (error) {
    showMessage('Login failed', 'error');
  }
}

async function handleRegister(event) {
  event.preventDefault();
  const userData = {
    email: document.getElementById('reg-email').value,
    username: document.getElementById('reg-username').value,
    first_name: document.getElementById('reg-firstname').value,
    last_name: document.getElementById('reg-lastname').value,
    password: document.getElementById('reg-password').value,
  };

  try {
    const response = await fetch('/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(userData),
    });

    const data = await response.json();
    if (response.ok) {
      hideAuthModal();
      showMessage('Registration successful! Please login.', 'success');
      // Clear form
      registerForm.reset();
      // Switch to login form
      switchAuthForm('login');
    } else {
      showMessage(data.detail || 'Registration failed', 'error');
    }
  } catch (error) {
    showMessage('Registration failed', 'error');
  }
}

function logout() {
  currentUser = null;
  currentToken = null;
  localStorage.removeItem('token');
  showAuthButtons();
  showMessage('Logged out successfully', 'success');
}

async function fetchUserProfile() {
  try {
    const response = await authenticatedFetch('/users/me');
    const user = await response.json();
    if (response.ok) {
      showUserInfo(user);
    } else {
      logout();
    }
  } catch (error) {
    logout();
  }
}

// Navigation functions
function showSection(sectionName) {
  // Hide all sections
  const sections = [activitiesSection, projectsSection, teamsSection, achievementsSection, workshopsSection, resourcesSection, profileSection];
  sections.forEach(section => section.classList.add('hidden'));

  // Remove active class from nav items
  const navItems = [navActivities, navProjects, navTeams, navAchievements, navWorkshops, navResources, navProfile];
  navItems.forEach(item => item.classList.remove('active'));

  // Show selected section and set active nav
  switch (sectionName) {
    case 'activities':
      activitiesSection.classList.remove('hidden');
      navActivities.classList.add('active');
      fetchActivities();
      break;
    case 'projects':
      projectsSection.classList.remove('hidden');
      navProjects.classList.add('active');
      fetchProjects();
      break;
    case 'teams':
      teamsSection.classList.remove('hidden');
      navTeams.classList.add('active');
      fetchTeams();
      break;
    case 'achievements':
      achievementsSection.classList.remove('hidden');
      navAchievements.classList.add('active');
      fetchAchievements();
      break;
    case 'workshops':
      workshopsSection.classList.remove('hidden');
      navWorkshops.classList.add('active');
      fetchWorkshops();
      break;
    case 'resources':
      resourcesSection.classList.remove('hidden');
      navResources.classList.add('active');
      fetchResources();
      break;
    case 'profile':
      profileSection.classList.remove('hidden');
      navProfile.classList.add('active');
      loadProfile();
      break;
  }
}

// API functions
async function authenticatedFetch(url, options = {}) {
  const headers = {
    'Authorization': `Bearer ${currentToken}`,
    ...options.headers,
  };

  return fetch(url, {
    ...options,
    headers,
  });
}

function showMessage(message, type) {
  // Remove existing message
  const existingMessage = document.querySelector('.message');
  if (existingMessage) {
    existingMessage.remove();
  }

  // Create new message
  const messageDiv = document.createElement('div');
  messageDiv.className = `message ${type}`;
  messageDiv.textContent = message;

  // Add to page
  document.body.appendChild(messageDiv);

  // Auto remove after 5 seconds
  setTimeout(() => {
    if (messageDiv.parentNode) {
      messageDiv.remove();
    }
  }, 5000);
}

// Activities functions
async function fetchActivities() {
  try {
    const response = await fetch('/activities');
    const activities = await response.json();

    activitiesList.innerHTML = '';

    activities.forEach(activity => {
      const activityCard = document.createElement('div');
      activityCard.className = 'activity-card';

      const spotsLeft = activity.max_participants - activity.participant_count;
      const isSignedUp = currentUser && activity.participants?.some(p => p.id === currentUser.id);

      activityCard.innerHTML = `
        <h4>${activity.name}</h4>
        <p>${activity.description}</p>
        <p><strong>Schedule:</strong> ${activity.schedule}</p>
        <p><strong>Availability:</strong> ${spotsLeft} spots left</p>
        <div class="activity-actions">
          ${currentUser ? (isSignedUp ?
            `<button class="btn btn-danger" onclick="unregisterFromActivity(${activity.id})">Unregister</button>` :
            `<button class="btn btn-primary" onclick="signupForActivity(${activity.id})">Sign Up</button>`
          ) : '<p class="text-muted">Login to sign up</p>'}
        </div>
      `;

      activitiesList.appendChild(activityCard);
    });
  } catch (error) {
    activitiesList.innerHTML = '<p>Failed to load activities</p>';
  }
}

async function signupForActivity(activityId) {
  try {
    const response = await authenticatedFetch(`/activities/${activityId}/signup`, {
      method: 'POST',
    });

    const result = await response.json();
    if (response.ok) {
      showMessage(result.message, 'success');
      fetchActivities();
    } else {
      showMessage(result.detail || 'Signup failed', 'error');
    }
  } catch (error) {
    showMessage('Signup failed', 'error');
  }
}

async function unregisterFromActivity(activityId) {
  try {
    const response = await authenticatedFetch(`/activities/${activityId}/unregister`, {
      method: 'DELETE',
    });

    const result = await response.json();
    if (response.ok) {
      showMessage(result.message, 'success');
      fetchActivities();
    } else {
      showMessage(result.detail || 'Unregister failed', 'error');
    }
  } catch (error) {
    showMessage('Unregister failed', 'error');
  }
}

// Projects functions
async function fetchProjects() {
  try {
    const response = await fetch('/projects');
    const projects = await response.json();

    projectsList.innerHTML = '';

    projects.forEach(project => {
      const projectCard = document.createElement('div');
      projectCard.className = 'project-card';

      projectCard.innerHTML = `
        <h4>${project.title}</h4>
        <p>${project.description}</p>
        <p><strong>Members:</strong> ${project.member_count}</p>
        <p><strong>Created by:</strong> ${project.created_by}</p>
        ${project.url ? `<p><strong>URL:</strong> <a href="${project.url}" target="_blank">${project.url}</a></p>` : ''}
      `;

      projectsList.appendChild(projectCard);
    });

    // Show create project form if user is logged in
    if (currentUser) {
      createProject.classList.remove('hidden');
    }
  } catch (error) {
    projectsList.innerHTML = '<p>Failed to load projects</p>';
  }
}

async function handleCreateProject(event) {
  event.preventDefault();

  const projectData = {
    title: document.getElementById('project-title').value,
    description: document.getElementById('project-description').value,
    url: document.getElementById('project-url').value || null,
  };

  try {
    const response = await authenticatedFetch('/projects', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(projectData),
    });

    const result = await response.json();
    if (response.ok) {
      showMessage(result.message, 'success');
      projectForm.reset();
      fetchProjects();
    } else {
      showMessage(result.detail || 'Failed to create project', 'error');
    }
  } catch (error) {
    showMessage('Failed to create project', 'error');
  }
}

// Teams functions
async function fetchTeams() {
  try {
    const response = await fetch('/teams');
    const teams = await response.json();

    teamsList.innerHTML = '';

    teams.forEach(team => {
      const teamCard = document.createElement('div');
      teamCard.className = 'team-card';

      teamCard.innerHTML = `
        <h4>${team.name}</h4>
        <p>${team.description}</p>
        <p><strong>Members:</strong> ${team.member_count}</p>
      `;

      teamsList.appendChild(teamCard);
    });

    // Show create team form if user is logged in
    if (currentUser) {
      createTeam.classList.remove('hidden');
    }
  } catch (error) {
    teamsList.innerHTML = '<p>Failed to load teams</p>';
  }
}

async function handleCreateTeam(event) {
  event.preventDefault();

  const teamData = {
    name: document.getElementById('team-name').value,
    description: document.getElementById('team-description').value,
  };

  try {
    const response = await authenticatedFetch('/teams', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(teamData),
    });

    const result = await response.json();
    if (response.ok) {
      showMessage(result.message, 'success');
      teamForm.reset();
      fetchTeams();
    } else {
      showMessage(result.detail || 'Failed to create team', 'error');
    }
  } catch (error) {
    showMessage('Failed to create team', 'error');
  }
}

// Achievements functions
async function fetchAchievements() {
  try {
    const response = await fetch('/achievements');
    const achievements = await response.json();

    achievementsList.innerHTML = '';

    achievements.forEach(achievement => {
      const achievementCard = document.createElement('div');
      achievementCard.className = 'achievement-card';

      achievementCard.innerHTML = `
        <h4>${achievement.title}</h4>
        <p>${achievement.description}</p>
        <p><strong>Type:</strong> ${achievement.type}</p>
        ${achievement.organization ? `<p><strong>Organization:</strong> ${achievement.organization}</p>` : ''}
        <p><strong>User:</strong> ${achievement.user}</p>
      `;

      achievementsList.appendChild(achievementCard);
    });

    // Show create achievement form if user is logged in
    if (currentUser) {
      createAchievement.classList.remove('hidden');
    }
  } catch (error) {
    achievementsList.innerHTML = '<p>Failed to load achievements</p>';
  }
}

async function handleCreateAchievement(event) {
  event.preventDefault();

  const achievementData = {
    title: document.getElementById('achievement-title').value,
    description: document.getElementById('achievement-description').value,
    achievement_type: document.getElementById('achievement-type').value,
    organization: document.getElementById('achievement-org').value || null,
  };

  try {
    const response = await authenticatedFetch('/achievements', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(achievementData),
    });

    const result = await response.json();
    if (response.ok) {
      showMessage(result.message, 'success');
      achievementForm.reset();
      fetchAchievements();
    } else {
      showMessage(result.detail || 'Failed to add achievement', 'error');
    }
  } catch (error) {
    showMessage('Failed to add achievement', 'error');
  }
}

// Workshops functions
async function fetchWorkshops() {
  try {
    const response = await fetch('/workshops');
    const workshops = await response.json();

    workshopsList.innerHTML = '';

    workshops.forEach(workshop => {
      const workshopCard = document.createElement('div');
      workshopCard.className = 'workshop-card';

      workshopCard.innerHTML = `
        <h4>${workshop.name}</h4>
        <p>${workshop.overview}</p>
        <p><strong>Level:</strong> ${workshop.level}</p>
        <p><strong>Seats Available:</strong> ${workshop.seats_available}</p>
        ${workshop.trainer ? `<p><strong>Trainer:</strong> ${workshop.trainer}</p>` : ''}
      `;

      workshopsList.appendChild(workshopCard);
    });

    // Show create workshop form if user is logged in
    if (currentUser) {
      createWorkshop.classList.remove('hidden');
    }
  } catch (error) {
    workshopsList.innerHTML = '<p>Failed to load workshops</p>';
  }
}

async function handleCreateWorkshop(event) {
  event.preventDefault();

  const workshopData = {
    name: document.getElementById('workshop-name').value,
    overview: document.getElementById('workshop-overview').value,
    level: document.getElementById('workshop-level').value,
    number_of_seats: parseInt(document.getElementById('workshop-seats').value),
  };

  try {
    const response = await authenticatedFetch('/workshops', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(workshopData),
    });

    const result = await response.json();
    if (response.ok) {
      showMessage(result.message, 'success');
      workshopForm.reset();
      fetchWorkshops();
    } else {
      showMessage(result.detail || 'Failed to create workshop', 'error');
    }
  } catch (error) {
    showMessage('Failed to create workshop', 'error');
  }
}

// Resources functions
async function fetchResources() {
  try {
    const response = await fetch('/resources');
    const resources = await response.json();

    resourcesList.innerHTML = '';

    resources.forEach(resource => {
      const resourceCard = document.createElement('div');
      resourceCard.className = 'resource-card';

      resourceCard.innerHTML = `
        <h4>${resource.name}</h4>
        <p>${resource.description}</p>
        <p><strong>Category:</strong> ${resource.category}</p>
        ${resource.link ? `<p><strong>Link:</strong> <a href="${resource.link}" target="_blank">${resource.link}</a></p>` : ''}
        <p><strong>Added by:</strong> ${resource.created_by}</p>
      `;

      resourcesList.appendChild(resourceCard);
    });

    // Show create resource form if user is logged in
    if (currentUser) {
      createResource.classList.remove('hidden');
    }
  } catch (error) {
    resourcesList.innerHTML = '<p>Failed to load resources</p>';
  }
}

async function handleCreateResource(event) {
  event.preventDefault();

  const resourceData = {
    name: document.getElementById('resource-name').value,
    description: document.getElementById('resource-description').value,
    category_name: document.getElementById('resource-category').value,
    link: document.getElementById('resource-link').value || null,
  };

  try {
    const response = await authenticatedFetch('/resources', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(resourceData),
    });

    const result = await response.json();
    if (response.ok) {
      showMessage(result.message, 'success');
      resourceForm.reset();
      fetchResources();
    } else {
      showMessage(result.detail || 'Failed to add resource', 'error');
    }
  } catch (error) {
    showMessage('Failed to add resource', 'error');
  }
}

// Profile functions
async function loadProfile() {
  try {
    const response = await authenticatedFetch('/users/me');
    const user = await response.json();

    profileContent.innerHTML = `
      <div class="profile-info">
        <h4>${user.first_name} ${user.last_name}</h4>
        <p><strong>Username:</strong> ${user.username}</p>
        <p><strong>Email:</strong> ${user.email}</p>
        ${user.bio ? `<p><strong>Bio:</strong> ${user.bio}</p>` : ''}
        ${user.year ? `<p><strong>Year:</strong> ${user.year}</p>` : ''}
        ${user.github ? `<p><strong>GitHub:</strong> <a href="${user.github}" target="_blank">${user.github}</a></p>` : ''}
        ${user.linkedin ? `<p><strong>LinkedIn:</strong> <a href="${user.linkedin}" target="_blank">${user.linkedin}</a></p>` : ''}
        ${user.twitter ? `<p><strong>Twitter:</strong> <a href="${user.twitter}" target="_blank">${user.twitter}</a></p>` : ''}
        <p><strong>Role:</strong> ${user.is_mentor ? 'Mentor' : 'Student'} ${user.is_admin ? '(Admin)' : ''}</p>
        <p><strong>Member since:</strong> ${new Date(user.created_at).toLocaleDateString()}</p>
      </div>
    `;

    // Load attendance stats
    loadAttendanceStats();
  } catch (error) {
    profileContent.innerHTML = '<p>Failed to load profile</p>';
  }
}

async function loadAttendanceStats() {
  try {
    const response = await authenticatedFetch('/attendance/stats');
    const stats = await response.json();

    attendanceStats.innerHTML = `
      <h5>Attendance Statistics</h5>
      <p><strong>Total Days:</strong> ${stats.total_days}</p>
      <p><strong>Present Days:</strong> ${stats.present_days}</p>
      <p><strong>Absent Days:</strong> ${stats.absent_days}</p>
      <p><strong>Attendance Percentage:</strong> ${stats.attendance_percentage}%</p>
    `;
  } catch (error) {
    attendanceStats.innerHTML = '<p>Failed to load attendance stats</p>';
  }
}

async function markAttendance(present) {
  try {
    const response = await authenticatedFetch('/attendance', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ present }),
    });

    const result = await response.json();
    if (response.ok) {
      showMessage(result.message, 'success');
      loadAttendanceStats();
    } else {
      showMessage(result.detail || 'Failed to mark attendance', 'error');
    }
  } catch (error) {
    showMessage('Failed to mark attendance', 'error');
  }
}

      // Hide message after 5 seconds
      setTimeout(() => {
        messageDiv.classList.add("hidden");
      }, 5000);
    } catch (error) {
      messageDiv.textContent = "Failed to unregister. Please try again.";
      messageDiv.className = "error";
      messageDiv.classList.remove("hidden");
      console.error("Error unregistering:", error);
    }
  }

  // Handle form submission
  signupForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const email = document.getElementById("email").value;
    const activity = document.getElementById("activity").value;

    try {
      const response = await fetch(
        `/activities/${encodeURIComponent(
          activity
        )}/signup?email=${encodeURIComponent(email)}`,
        {
          method: "POST",
        }
      );

      const result = await response.json();

      if (response.ok) {
        messageDiv.textContent = result.message;
        messageDiv.className = "success";
        signupForm.reset();

        // Refresh activities list to show updated participants
        fetchActivities();
      } else {
        messageDiv.textContent = result.detail || "An error occurred";
        messageDiv.className = "error";
      }

      messageDiv.classList.remove("hidden");

      // Hide message after 5 seconds
      setTimeout(() => {
        messageDiv.classList.add("hidden");
      }, 5000);
    } catch (error) {
      messageDiv.textContent = "Failed to sign up. Please try again.";
      messageDiv.className = "error";
      messageDiv.classList.remove("hidden");
      console.error("Error signing up:", error);
    }
  });

  // Initialize app
  fetchActivities();
});
