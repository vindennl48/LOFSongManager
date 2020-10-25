def dev(name):
    try:
        import development

        if not development.DEVELOPMENT:
            return False

        if name == "DEVELOPMENT":
            return development.DEVELOPMENT

        return development.flags[name]

    except:
        return False
