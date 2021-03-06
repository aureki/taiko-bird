Background = {}

function Background:load()
    self.img = love.graphics.newImage("assets/coolbackground.png")
    self.nightImg = love.graphics.newImage("assets/coolnightbackground.png")
    self.x = 0
    self.xSpeed = -3 * utils.vh
    self.shader = nil

    self:createDarkenShader()
end

-- Representa, de 0 a 1, o quão "noite" está.
function Background:nightIntensity(mockTime)
    local time = mockTime or os.time()
    local dateTable = os.date("*t", time)
    local minutesInsideDay = dateTable.hour * 60 + dateTable.min
    local darkMinutesAroundMidnight = 6 * 60

    if dateTable.hour < 12 then
        distanceFromMidnight = minutesInsideDay
    else
        distanceFromMidnight = 24 * 60 - minutesInsideDay
    end

    return math.max(0, 1 - distanceFromMidnight / darkMinutesAroundMidnight)
end

function Background:createDarkenShader()
    local darkenIntensity = self:nightIntensity() * 0.4
    self.shader = Shaders.newDarkenShader(darkenIntensity)
end

function Background:update(dt)
    self.x = self.x + self.xSpeed * dt
end

function Background:draw()
    -- Calcula a escala minima que vai cobrir a tela toda
    local scaleX = love.graphics.getWidth() / self.img:getWidth()
    local scaleY = love.graphics.getHeight() / self.img:getHeight()

    local scale = math.max(scaleX, scaleY)
    local scaledWidth = self.img:getWidth() * scale

    local imageToDraw = self.img
    if self:nightIntensity() > 0 then
        imageToDraw = self.nightImg
    end

    -- Como o self.x pode diminuir infinitamente, temos que limitar até um máximo de -scaledWidth
    local leftBackgroundXPosition = math.fmod(self.x, scaledWidth)

    love.graphics.setShader(self.shader)
        love.graphics.draw(imageToDraw, leftBackgroundXPosition, 0, 0, scale, scale)
        love.graphics.draw(imageToDraw, leftBackgroundXPosition + scaledWidth, 0, 0, scale, scale)
    love.graphics.setShader()
end

-- BOA LINDA! ヾ(≧▽≦*)o
-- obg amor
-- aff vou deixar isso mt fof