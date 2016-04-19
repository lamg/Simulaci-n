import sqlite3


def substring(chain, lo, hi):
    c = str(chain)
    res = ""
    for i in range(lo, hi):
        res += c[i]
    return res


def normal_distribution(prob):

    z = -6
    connection = sqlite3.connect('simulacion.db')

    cursor = connection.execute('SELECT z FROM normal_dist WHERE prob = %s' % (str(prob)))
    try:
        for z_val in cursor:
            z = float(z_val[0])

        if z == -6:
            x = float(prob)
            y = float(prob)

            while True:
                x += 0.0001
                y += 0.0001

                px = substring(x, 0, 6)
                py = substring(y, 0, 6)

                cursor = connection.execute('SELECT z FROM normal_dist WHERE prob = %s' % (str(px)))
                for z_val in cursor:
                    z = float(z_val[0])

                if z != -6:
                    return z

                cursor = connection.execute('SELECT z FROM normal_dist WHERE prob = %s' % (str(py)))
                for z_val in cursor:
                    z = float(z_val[0])

                if z != -6:
                    return z
    except:
        print("Error occurred while searching for z value.")
        return

    finally:
        connection.close()
    return z


def ji_squared_distribution(alpha, freedom_degrees):
    prob_value = 0

    connection = sqlite3.connect('simulacion.db')
    try:
        cursor = connection.execute(
            'SELECT prob FROM chi_dist WHERE alpha = %s AND grado_lib = %s' % (str(alpha), str(freedom_degrees)))

        for item in cursor:
            prob_value = float(item[0])

    except:
        print("Error occurred while searching for probability value value: %s")
        return
    finally:
        connection.close()

    return prob_value
