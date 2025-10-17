#اضافه کردن کتابخانه های مورد نیاز پروژه 
import random #برای تولید اعداد و نمونه‌های تصادفی
import time #برای اندازه‌گیری زمان اجرای الگوریتم
import networkx as nx #برای ساخت و پردازش گراف‌ها
import numpy as np #برای محاسبات عددی

#تعریف تابع شبیه‌سازی کاهش دما
#Max_Node = حداکثر تعداد رأس‌هایی که می‌توانند در پوشش قرار بگیرند
#initial_temp = دمای اولیه الگوریتم
#colling_rate = نرخ کاهش دما در هر تکرار
#max_iteration = حداکثر تعداد تکرار
def simulated_annealing_VertexCover(graph, Max_Node, initial_temp=1500, cooling_rate=0.95, max_iteration=1500):

    #استخراج داده‌های گراف
    nodes_of_graph = list(graph.nodes) #لیست راس های گراف
    edges_of_graph = set(graph.edges) #مجموعه یال های گراف

    #ایجاد یک پوشش اولیه تصادفی
    current_solution = set(random.sample(nodes_of_graph, Max_Node))
    best_solution = current_solution.copy() #بهترین جواب فعلی (در ابتدا همان راه‌حل اولیه است)

    #تابع محاسبه یال های پوشش داده شده از گراف
    #cover = لیست رأس‌های موجود در پوشش
    #خروجی تایع زیر تعداد یال‌هایی است که حداقل یکی از رأس‌هایشان در پوشش قرار دارد
    def count_covered_edges(cover):
        return len([edge for edge in edges_of_graph if edge[0] in cover or edge[1] in cover])

    #تعداد یال‌هایی که توسط بهترین پوشش فعلی پوشش داده شده‌اند
    best_covered = count_covered_edges(best_solution)
    #مقدار اولیه دما
    current_temp = initial_temp

    for i in range(max_iteration):
        # یک رأس تصادفی از پوشش فعلی برای حذف
        node_out = random.choice(list(current_solution))
        #یک رأس تصادفی که هنوز در پوشش نیست، برای اضافه شدن
        node_in = random.choice([node for node in nodes_of_graph if node not in current_solution])

        # راه حل جدید با حذف یک نود و درج یک نود دیگر
        new_solution = current_solution.copy()
        new_solution.remove(node_out)
        new_solution.add(node_in)

        # محاسبه تعداد یال‌های پوشش داده شده توسط راه‌حل جدید
        new_covered = count_covered_edges(new_solution)

        #تصمیم‌گیری برای قبول یا رد راه‌حل جدید
        # new_best_difference = تفاوت بین تعداد یال‌های پوشش داده شده در راه‌حل جدید و بهترین راه‌حل
        new_best_difference = new_covered - best_covered
        if new_best_difference > 0 or random.random() < np.exp(new_best_difference / current_temp):
            current_solution = new_solution
            if new_covered > best_covered:
                best_solution = current_solution
                best_covered = new_covered

        # کاهش دما
        current_temp *= cooling_rate

    return list(best_solution), best_covered


# تابعی برای اجرای آزمایش روی چندین گراف
def run_algorithm(graph_files, Max_Node_values):
    results = {}
    for name, path in graph_files.items():
        graph = nx.read_gexf(path)
        Max_Node = Max_Node_values.get(name, None)
        if Max_Node:
            start_time = time.time()
            cover, covered_edges = simulated_annealing_VertexCover(graph, Max_Node)
            runtime = time.time() - start_time
            results[name] = {
                "Covered Edges": covered_edges,
                "Runtime (s)": runtime,
                "Vertex Cover": cover
            }
    return results


# مسیر فایل های مربوط به گراف ها
graph_files = {
    "yeast": "C:\\Users\\Hossein\\Desktop\\datasets\\yeast.gexf",
    "eurosis": "C:\\Users\\Hossein\\Desktop\\datasets\\EuroSiS Generale Pays.gexf",
    "codeminer": "C:\\Users\\Hossein\\Desktop\\datasets\\codeminer.gexf",
    "cpan-authors": "C:\\Users\\\Hossein\Desktop\\datasets\\cpan-authors.gexf"
}

# مقدار حداکثر یال پوششی برای هر گراف
Max_Node_values = {
    "codeminer": 191,
    "cpan-authors": 116,
    "eurosis": 597,
    "yeast": 763
}

results = run_algorithm(graph_files, Max_Node_values)

# نمایش نتایج
for name, result in results.items():
    print(f"Graph: {name}")
    print(f"Covered Edges: {result['Covered Edges']} Edges")
    print(f"Runtime: {result['Runtime (s)']} seconds \n")
