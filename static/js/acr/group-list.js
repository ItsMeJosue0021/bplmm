const tabs = ['tab1', 'tab2'];

tabs.forEach(tab => {
    const tabLink = document.getElementById(`${tab}-link`);
    const otherTab = tabs.find(t => t !== tab);

    tabLink.addEventListener('click', function (event) {
        event.preventDefault();
        setActiveTab(tab, otherTab);
    });
});

function setActiveTab(activeTab, inactiveTab) {
    document.getElementById(activeTab).style.display = 'block';
    document.getElementById(inactiveTab).style.display = 'none';

    const activeTabLink = document.getElementById(`${activeTab}-link`);
    const inactiveTabLink = document.getElementById(`${inactiveTab}-link`);

    activeTabLink.classList.replace('bg-primary', 'bg-white');
    activeTabLink.classList.remove('text-white');

    inactiveTabLink.classList.replace('bg-white', 'bg-primary');
    inactiveTabLink.classList.add('text-white');
}