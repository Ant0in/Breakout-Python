class GameBox:

    def __init__(self, width: float, height: float) -> None:
        """
        Initialise une box de jeu avec une largeur et une hauteur données.
        """
        self._width = width
        self._height = height
        self._entities: list[SolidInterface] = []

    def getWidth(self) -> float:
        return self._width

    def getHeight(self) -> float:
        return self._height

    def addEntity(self, entity: SolidInterface) -> None:
        """
        Ajoute une entité dans la box.
        """
        self._entities.append(entity)

    def getEntities(self) -> list[SolidInterface]:
        """
        Retourne la liste des entités présentes dans la box.
        """
        return self._entities

    def isOutOfBounds(self, entity: SolidInterface) -> bool:
        """
        Vérifie si une entité est hors des limites de la box.
        """
        if isinstance(entity, SolidRectangle):
            rect = entity
            return (
                rect.getPosition().getX() < 0 or
                rect.getPosition().getY() < 0 or
                rect.getPosition().getX() + rect.getWidth() > self.getWidth() or
                rect.getPosition().getY() + rect.getHeight() > self.getHeight()
            )
        elif isinstance(entity, SolidCircle):
            circle = entity
            return (
                circle.getPosition().getX() - circle.getRadius() < 0 or
                circle.getPosition().getY() - circle.getRadius() < 0 or
                circle.getPosition().getX() + circle.getRadius() > self.getWidth() or
                circle.getPosition().getY() + circle.getRadius() > self.getHeight()
            )
        else:
            raise NotImplementedError("Type d'entité non supporté pour isOutOfBounds.")

    def checkCollisions(self) -> list[tuple[SolidInterface, SolidInterface]]:
        """
        Vérifie les collisions entre toutes les entités dans la box.
        Retourne une liste de tuples représentant les paires d'entités en collision.
        """
        collisions = []
        for i, entity1 in enumerate(self._entities):
            for entity2 in self._entities[i + 1:]:
                if CollisionHelper.isColliding(entity1, entity2):
                    collisions.append((entity1, entity2))
        return collisions

    def update(self) -> None:
        """
        Met à jour l'état de la box :
        - Vérifie les entités hors limites.
        - Détecte les collisions.
        """
        for entity in self._entities:
            if self.isOutOfBounds(entity):
                print(f"Entity {entity} is out of bounds!")

        collisions = self.checkCollisions()
        for e1, e2 in collisions:
            print(f"Collision detected between {e1} and {e2}!")
